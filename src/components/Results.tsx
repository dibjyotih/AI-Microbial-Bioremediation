import type { MicrobeResult } from "../App";
import "./Results.css";

interface Props {
  results: MicrobeResult[];
}

export default function Results({ results }: Props) {
  if (!results.length) return null;

  return (
    <div className="report-container">
      <h2 className="report-header">Bioremediation Report</h2>
      <div className="report-content">
        {results.map((result, index) => (
          <div key={index} className="plastic-report">
            <h3 className="plastic-header">
              Plastic Type: {result.Plastic_Type} ({result.count || 1} sample{result.count !== 1 ? "s" : ""})
            </h3>
            <div className="report-item">
              <span className="report-label">Recommended Microbe</span>
              <span className="report-value microbe">{result.Recommended_Microbe}</span>
            </div>
            <div className="report-item">
              <span className="report-label">Optimal pH</span>
              <span className="report-value">{result.Optimal_pH}</span>
            </div>
            <div className="report-item">
              <span className="report-label">Optimal Temperature</span>
              <span className="report-value">{result.Optimal_Temp}</span>
            </div>
            <div className="report-item">
              <span className="report-label">Degradation Progress</span>
              <span className="report-value progress">{result.Degradation_Progress}</span>
            </div>
            <div className="report-message">
              <p>{result.Message}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}