export interface AuditResult {
  control_id: string;
  description: string;
  level?: number | null;
  result?: string | null;
  duration?: string | null;
}

export interface AuditRun {
  run_id: string;
  started_at: string;
  completed_at?: string | null;
  status: "running" | "completed" | "failed";
  benchmark: {
    platform: string;
    version: string;
  };
  level: number;
  system_type: string;
  execution_mode: string;
  summary: Record<string, number>;
  results: AuditResult[];
  error_message?: string | null;
}

export interface AuditRequestPayload {
  benchmark?: {
    platform?: string;
    version?: string;
  };
  includes?: string[];
  excludes?: string[];
  level?: number;
  system_type?: "server" | "workstation";
  execution_mode?: "quick" | "full";
  log_level?: "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL";
}
