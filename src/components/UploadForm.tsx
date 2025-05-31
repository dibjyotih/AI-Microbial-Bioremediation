import { useState } from "react";
import axios from "axios";
import type { MicrobeResult } from "../App";
import "./UploadForm.css";

interface Props {
  setResults: (data: MicrobeResult[]) => void;
}

export default function UploadForm({ setResults }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file.");
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const text = await file.text();
      const lines = text.trim().split("\n");
      if (lines.length < 2) {
        setError("CSV must have headers and at least one data row.");
        setLoading(false);
        return;
      }

      const headers = lines[0].split(",").map((h) => h.trim());
      if (headers.length !== 10 || headers.some((h, i) => h !== `band${i + 1}`)) {
        setError("CSV must have headers: band1 to band10.");
        setLoading(false);
        return;
      }

      const rawResults: MicrobeResult[] = [];
      for (let i = 1; i < lines.length; i++) {
        const data = lines[i].split(",").map((v) => parseFloat(v.trim()));
        if (data.length !== 10 || data.some(isNaN)) {
          setError(`Row ${i} must have 10 numeric spectral bands (band1 to band10).`);
          setLoading(false);
          return;
        }

        const spectralData = headers.reduce((obj, header, idx) => {
          obj[header] = data[idx];
          return obj;
        }, {} as Record<string, number>);

        const plasticRes = await axios.post<{ plastic_type: string }>(
          "http://127.0.0.1:5000/identify_plastic",
          spectralData
        );
        const plasticType = plasticRes.data.plastic_type;

        const microbeRes = await axios.post<{
          recommended: string;
          optimal_pH: number;
          optimal_temp: number;
        }>("http://127.0.0.1:5000/recommend_microbe", {
          plastic_type: plasticType,
          pH: 7.2,
          temp: 32,
        });

        const microbe = microbeRes.data.recommended;
        const optimalPH = microbeRes.data.optimal_pH;
        const optimalTemp = microbeRes.data.optimal_temp;

        if (microbe.startsWith("Error:") || microbe.startsWith("No suitable microbe")) {
          rawResults.push({
            Plastic_Type: plasticType,
            Recommended_Microbe: microbe,
            Degradation_Progress: "0%",
            Message: "Unable to monitor degradation due to recommendation error",
            Optimal_pH: optimalPH.toString(),
            Optimal_Temp: `${optimalTemp}°C`,
          });
          continue;
        }

        const degradationRequestBody = {
          plastic_type: plasticType,
          microbe,
          elapsed_time: 30,
          pH: optimalPH,
          temp: optimalTemp,
        };
        console.log(`Sending to /monitor_degradation for row ${i}:`, degradationRequestBody);

        const degradationRes = await axios.post<{
          progress: number;
          message: string;
        }>("http://127.0.0.1:5000/monitor_degradation", degradationRequestBody);

        rawResults.push({
          Plastic_Type: plasticType,
          Recommended_Microbe: microbe,
          Degradation_Progress: `${(degradationRes.data.progress * 100).toFixed(1)}%`,
          Message: degradationRes.data.message,
          Optimal_pH: optimalPH.toString(),
          Optimal_Temp: `${optimalTemp}°C`,
        });
      }

      // Group results by Plastic_Type
      const groupedResults: { [key: string]: MicrobeResult } = {};
      rawResults.forEach((result) => {
        const key = result.Plastic_Type;
        if (!groupedResults[key]) {
          groupedResults[key] = { ...result, count: 1 };
        } else {
          groupedResults[key].count = (groupedResults[key].count || 0) + 1;
          const currentProgress = parseFloat(groupedResults[key].Degradation_Progress);
          const newProgress = parseFloat(result.Degradation_Progress);
          if (newProgress > currentProgress) {
            groupedResults[key] = { ...result, count: groupedResults[key].count };
          }
        }
      });

      const finalResults = Object.values(groupedResults);
      setResults(finalResults);
    } catch (error) {
      console.error("API call failed", error);
      setError("Failed to process data. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form">
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="file-input"
      />
      <button className="predict-button" onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Predict Microbes"}
      </button>
      {error && <p className="error-message">{error}</p>}
      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Analyzing samples...</p>
        </div>
      )}
    </div>
  );
}