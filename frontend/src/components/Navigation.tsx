import { FC } from "react";

interface NavigationProps {
  lastUpdated?: string;
  totalRuns?: number;
}

const Navigation: FC<NavigationProps> = ({ lastUpdated, totalRuns }) => {
  return (
    <header className="app-nav">
      <div className="brand">
        <strong>NovaShield</strong>
        <span>Next-gen CIS compliance observatory</span>
      </div>
      <div className="actions">
        {typeof totalRuns === "number" && totalRuns > 0 && (
          <span className="badge info">{totalRuns} runs logged</span>
        )}
        {lastUpdated && <span className="badge pass">Last update {lastUpdated}</span>}
      </div>
    </header>
  );
};

export default Navigation;
