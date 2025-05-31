import { useState } from "react";
import UploadForm from "./components/UploadForm";
import Results from "./components/Results";
import "./App.css";

// Define MicrobeResult with explicit properties
export type MicrobeResult = {
  Plastic_Type: string;
  Recommended_Microbe: string;
  Degradation_Progress: string;
  Message: string;
  Optimal_pH: string;
  Optimal_Temp: string;
  count?: number; // Allow count as an optional number
};

function App() {
  const [results, setResults] = useState<MicrobeResult[]>([]);

  return (
    <div className="app-container">
      <h1 className="main-header">
        <span role="img" aria-label="DNA">🧬</span> Microplastic Bioremediation Predictor
      </h1>
      <div className="form-container">
        <UploadForm setResults={setResults} />
      </div>
      {results.length > 0 && <Results results={results} />}
    </div>
  );
}

export default App;