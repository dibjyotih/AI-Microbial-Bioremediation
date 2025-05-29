import { useState } from "react";
import axios from "axios";
import type{ MicrobeResult } from "../App";
import "./UploadForm.css";

interface Props {
  setResults: (data: MicrobeResult[]) => void;
}

export default function UploadForm({ setResults }: Props) {
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post<MicrobeResult[]>("http://localhost:8000/predict/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResults(res.data);
    } catch (error) {
      console.error("Upload failed", error);
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
      <button className="upload-button" onClick={handleUpload}>
        Predict Microbes
      </button>
    </div>
  );
}
