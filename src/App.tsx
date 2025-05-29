import { useState } from "react";
import UploadForm from "./components/UploadForm";
import Results from "./components/Results";
import "./App.css";

export type MicrobeResult = Record<string, string>;

function App() {
  const [results, setResults] = useState<MicrobeResult[]>([]);

  return (
    <div className="app-wrapper">
      <h1 className="main-heading">🧬 Microplastic Bioremediation Predictor</h1>
      <div className="form-box">
        <UploadForm setResults={setResults} />
      </div>
      <Results results={results} />
    </div>
  );
}

export default App;
