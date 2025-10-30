import { AuditRequestPayload, AuditRun } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {})
    },
    ...options
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getAudits(limit = 5): Promise<AuditRun[]> {
  return request<AuditRun[]>(`/api/audits?limit=${limit}`);
}

export function runAudit(payload: AuditRequestPayload): Promise<AuditRun> {
  return request<AuditRun>("/api/audits/run", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}
