import { FC } from "react";
import clsx from "clsx";

interface StatusBadgeProps {
  status: string;
}

const palette: Record<string, string> = {
  Pass: "badge pass",
  Fail: "badge fail",
  Error: "badge error",
  Skipped: "badge info",
  Manual: "badge info",
  "Not Implemented": "badge info"
};

const StatusBadge: FC<StatusBadgeProps> = ({ status }) => {
  const normalized = status || "Unknown";
  const className = palette[normalized] ?? clsx("badge", "info");
  return <span className={className}>{normalized}</span>;
};

export default StatusBadge;
