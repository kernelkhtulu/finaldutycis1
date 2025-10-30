import { useMemo } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Navigation from "./components/Navigation";
import RunAuditPanel from "./components/RunAuditPanel";
import AuditSummaryCard from "./components/AuditSummaryCard";
import AuditRunTable from "./components/AuditRunTable";
import { getAudits, runAudit } from "./api";
import { AuditRequestPayload, AuditRun } from "./types";

const AUDIT_QUERY_KEY = ["audits"];

function formatTimestamp(timestamp?: string | null): string | undefined {
  if (!timestamp) return undefined;
  try {
    return new Intl.DateTimeFormat(undefined, {
      dateStyle: "medium",
      timeStyle: "short"
    }).format(new Date(timestamp));
  } catch (error) {
    console.warn("Unable to format timestamp", error);
    return timestamp;
  }
}

function App() {
  const queryClient = useQueryClient();

  const { data: audits = [], isFetching } = useQuery<AuditRun[]>({
    queryKey: AUDIT_QUERY_KEY,
    queryFn: () => getAudits(5),
    staleTime: 30_000
  });

  const mutation = useMutation({
    mutationFn: (payload: AuditRequestPayload) => runAudit(payload),
    onSuccess: (run: AuditRun) => {
      queryClient.setQueryData<AuditRun[]>(AUDIT_QUERY_KEY, (existing = []) => {
        const next = [run, ...existing];
        return next.slice(0, 5);
      });
    }
  });

  const latest = audits[0];
  const summary = latest?.summary ?? {};
  const results = useMemo(() => latest?.results ?? [], [latest]);
  const lastUpdated = formatTimestamp(latest?.completed_at ?? latest?.started_at);

  const handleRun = (payload: AuditRequestPayload) => {
    mutation.mutate(payload);
  };

  return (
    <div className="app-shell">
      <Navigation lastUpdated={lastUpdated} totalRuns={audits.length || undefined} />
      <main className="app-main">
        <div className="grid two-column" style={{ marginBottom: "1.5rem" }}>
          <RunAuditPanel onRun={handleRun} isRunning={mutation.isPending} />
          <AuditSummaryCard summary={summary} />
        </div>
        {mutation.isError && (
          <div className="card" style={{ border: "1px solid rgba(220,38,38,0.2)" }}>
            <div className="section-title">
              <h2>Audit execution failed</h2>
            </div>
            <p style={{ color: "#991b1b" }}>{(mutation.error as Error).message}</p>
          </div>
        )}
        {isFetching && (
          <div className="card">
            <div className="section-title">
              <h2>Refreshing data</h2>
            </div>
            <p>Syncing the latest run history…</p>
          </div>
        )}
        <AuditRunTable results={results} />
      </main>
    </div>
  );
}

export default App;
