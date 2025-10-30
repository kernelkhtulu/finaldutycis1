import { FC, FormEvent, useMemo, useState } from "react";
import { AuditRequestPayload } from "../types";

interface RunAuditPanelProps {
  onRun: (payload: AuditRequestPayload) => void;
  isRunning: boolean;
}

const RunAuditPanel: FC<RunAuditPanelProps> = ({ onRun, isRunning }) => {
  const [executionMode, setExecutionMode] = useState<"quick" | "full">("quick");
  const [systemType, setSystemType] = useState<"server" | "workstation">("server");
  const [level, setLevel] = useState<number>(0);

  const description = useMemo(() => {
    return executionMode === "quick"
      ? "Quick runs benchmark hot-spots for near real-time insight."
      : "Full runs execute every control in the selected benchmark.";
  }, [executionMode]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const payload: AuditRequestPayload = {
      execution_mode: executionMode,
      system_type: systemType,
      level,
      log_level: "WARNING"
    };
    onRun(payload);
  };

  return (
    <div className="card">
      <div className="section-title">
        <h2>Trigger audit</h2>
      </div>
      <form className="grid" onSubmit={handleSubmit} style={{ gap: "1.25rem" }}>
        <label className="grid" style={{ gap: "0.35rem" }}>
          <span>Execution mode</span>
          <select
            value={executionMode}
            onChange={(event) => setExecutionMode(event.target.value as "quick" | "full")}
            style={{ padding: "0.75rem", borderRadius: "12px", border: "1px solid #cbd5f5" }}
          >
            <option value="quick">Quick insight</option>
            <option value="full">Full benchmark</option>
          </select>
          <small style={{ color: "#64748b" }}>{description}</small>
        </label>

        <label className="grid" style={{ gap: "0.35rem" }}>
          <span>System profile</span>
          <select
            value={systemType}
            onChange={(event) => setSystemType(event.target.value as "server" | "workstation")}
            style={{ padding: "0.75rem", borderRadius: "12px", border: "1px solid #cbd5f5" }}
          >
            <option value="server">Server</option>
            <option value="workstation">Workstation</option>
          </select>
        </label>

        <label className="grid" style={{ gap: "0.35rem" }}>
          <span>CIS level focus</span>
          <select
            value={level}
            onChange={(event) => setLevel(Number(event.target.value))}
            style={{ padding: "0.75rem", borderRadius: "12px", border: "1px solid #cbd5f5" }}
          >
            <option value={0}>All levels</option>
            <option value={1}>Level 1</option>
            <option value={2}>Level 2</option>
          </select>
        </label>

        <button className="btn" type="submit" disabled={isRunning}>
          {isRunning ? "Running…" : "Launch audit"}
        </button>
      </form>
    </div>
  );
};

export default RunAuditPanel;
