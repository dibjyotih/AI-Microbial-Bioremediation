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
      // Validate headers: must be band1, band2, ..., bandN
      if (!headers[0].startsWith('band') || headers.some((h, i) => h !== `band${i + 1}`)) {
        setError("CSV headers must be sequential: band1, band2, ...");
        setLoading(false);
        return;
      }

      const numBands = headers.length;
      const samples = [];
      for (let i = 1; i < lines.length; i++) {
        const data = lines[i].split(",").map((v) => parseFloat(v.trim()));
        if (data.length !== numBands || data.some(isNaN)) {
          setError(`Row ${i} must have ${numBands} numeric spectral bands (${headers.join(', ')}).`);
          setLoading(false);
          return;
        }

        const spectralData = headers.reduce((obj, header, idx) => {
          obj[header] = data[idx];
          return obj;
        }, {} as Record<string, number>);
        samples.push(spectralData);
      }

      const response = await axios.post<{
        report?: MicrobeResult[],
        result?: MicrobeResult,
        duration_sec: number
      }>(
        "http://127.0.0.1:5000/identify_plastic",
        samples
      );

      if (response.data.report) {
        setResults(response.data.report);
      } else if (response.data.result) {
        setResults([response.data.result]);
      } else {
        throw new Error("Invalid response format from server.");
      }
    } catch (error) {
      console.error("API call failed", error);
      setError(
        "Failed to process data. Error: " +
        ((error instanceof Error && error.message) ? error.message : "Unknown error")
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form">
      <h3>Upload Spectral Dataset</h3>
      <p>Please upload a CSV file with the following structure:</p>
      <ul>
        <li>Headers must be sequential: <code>band1, band2, band3, ...</code></li>
        <li>At least one band (<code>band1</code>) is required.</li>
        <li>Each row represents a sample with numeric spectral values.</li>
        <li>Single-sample or multi-sample datasets are supported.</li>
        <li>Example for 3 bands: <code>band1,band2,band3</code><br/>
            <code>0.25,0.24,0.26</code><br/>
            <code>0.18,0.19,0.17</code></li>
      </ul>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        className="file-input"
      />
      <button className="predict-button" onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Predict Microbe"}
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