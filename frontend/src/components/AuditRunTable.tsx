import { FC } from "react";
import StatusBadge from "./StatusBadge";
import { AuditResult } from "../types";

interface AuditRunTableProps {
  results: AuditResult[];
}

const AuditRunTable: FC<AuditRunTableProps> = ({ results }) => {
  if (!results.length) {
    return (
      <div className="card">
        <div className="section-title">
          <h2>Latest controls</h2>
        </div>
        <p>No audit has been executed yet.</p>
      </div>
    );
  }

  return (
    <div className="card" style={{ overflowX: "auto" }}>
      <div className="section-title">
        <h2>Latest controls</h2>
        <span className="badge error">{results.length} entries</span>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Control</th>
            <th>Description</th>
            <th>Level</th>
            <th>Status</th>
            <th>Duration</th>
          </tr>
        </thead>
        <tbody>
          {results.map((result, index) => (
            <tr key={`${result.control_id}-${index}`}>
              <td data-label="Control">{result.control_id}</td>
              <td data-label="Description">{result.description}</td>
              <td data-label="Level">{result.level ?? "-"}</td>
              <td data-label="Status">
                {result.result ? <StatusBadge status={result.result} /> : <span className="badge info">Info</span>}
              </td>
              <td data-label="Duration">{result.duration ?? "-"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AuditRunTable;
