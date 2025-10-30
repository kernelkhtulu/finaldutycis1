import { FC, useMemo } from "react";
import { ResponsiveContainer, Bar, BarChart, Tooltip, XAxis, YAxis } from "recharts";

interface AuditSummaryCardProps {
  summary: Record<string, number>;
}

const AuditSummaryCard: FC<AuditSummaryCardProps> = ({ summary }) => {
  const data = useMemo(() => {
    return Object.entries(summary)
      .filter(([key]) => key.toLowerCase() !== "total")
      .map(([key, value]) => ({ name: key, value }));
  }, [summary]);

  const total = summary.total ?? data.reduce((acc, item) => acc + item.value, 0);

  if (!data.length) {
    return (
      <div className="card">
        <div className="section-title">
          <h2>Compliance pulse</h2>
        </div>
        <p>No audit telemetry yet. Launch a run to populate the dashboard.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="section-title">
        <h2>Compliance pulse</h2>
        <div className="badge error">{total} checks assessed</div>
      </div>
      <div style={{ height: 240 }}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ left: 16, right: 16, top: 16, bottom: 16 }}>
            <XAxis type="number" allowDecimals={false} hide />
            <YAxis type="category" dataKey="name" width={80} />
            <Tooltip cursor={{ fill: "rgba(37,99,235,0.08)" }} />
            <Bar dataKey="value" radius={[6, 6, 6, 6]} fill="#1d4ed8" barSize={26} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default AuditSummaryCard;
