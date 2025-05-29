import  type{ MicrobeResult } from "../App";
import "./Results.css";

interface Props {
  results: MicrobeResult[];
}

export default function Results({ results }: Props) {
  if (!results.length) return null;

  return (
    <table className="results-table">
      <thead>
        <tr>
          {Object.keys(results[0]).map((key) => (
            <th key={key}>{key}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {results.map((row, idx) => (
          <tr key={idx}>
            {Object.values(row).map((val, i) => (
              <td key={i}>{val}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
