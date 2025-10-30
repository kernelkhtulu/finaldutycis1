# NovaShield

NovaShield is the next-generation evolution of the original CIS Benchmarks Audit script. It retains the trusted audit engine while wrapping it inside a modern platform composed of a FastAPI backend and a responsive React experience. The result is a realtime observatory for compliance teams—actionable insights, rich history, and effortless navigation across thousands of controls.

## Feature highlights

- **Next-gen UI:** A Vite + React dashboard with responsive cards, charts, and fluid navigation optimised for desktops and tablets.
- **FastAPI service layer:** An async-ready backend that exposes audit execution and history endpoints, with first-class CORS support for browser clients.
- **Zero-copy compliance engine:** The original `cis_audit` logic now powers NovaShield through a service wrapper, guaranteeing continuity with existing benchmark content.
- **Quick vs full runs:** Trigger rapid “pulse checks” with curated control sets or execute the full benchmark catalogue when you need exhaustive evidence.
- **Actionable telemetry:** Summaries roll up pass/fail/error counts, while detailed tables expose per-control outcomes, durations, and levels.

## Getting started

### Prerequisites

- Python **3.11+** for the backend service
- Node.js **18+** (or a compatible runtime) for the React interface

### Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

The API is served at `http://127.0.0.1:8000`. Useful endpoints include:

- `GET /health` – readiness probe
- `GET /api/audits?limit=5` – fetch recent runs (newest first)
- `POST /api/audits/run` – execute a new audit (see payload schema below)

Example request body:

```json
{
  "execution_mode": "quick",
  "system_type": "server",
  "level": 0
}
```

Quick mode automatically injects a curated set of high-signal controls. Supply `"execution_mode": "full"` and optional `includes` / `excludes` arrays when you need exhaustive coverage.

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

By default the UI assumes the backend is available on `http://localhost:8000`. Override the target host by setting `VITE_API_BASE_URL` before launching the dev server, e.g. `VITE_API_BASE_URL=https://api.example.com npm run dev`.

The dashboard provides:

- A **Trigger audit** panel to launch quick or full runs
- A **Compliance pulse** chart aggregating latest pass/fail/error counts
- A **Latest controls** table with rich status badges and durations

### Legacy CLI

Prefer the classic single-file workflow? The refreshed `cis_audit.py` remains in the repository and continues to run standalone audits:

```bash
python cis_audit.py --json --include 1.1.1.1 1.1.1.2
```

The script’s version has been bumped to **1.0.0**, the `--version` output is now well-formed, and authentication checks for emergency mode have been corrected.

## Testing

Run the FastAPI unit tests with:

```bash
pytest
```

This exercises the new orchestration layer and guards NovaShield’s quick-mode defaults and summary logic.

## Roadmap ideas

- Multi-platform benchmark catalogues (RHEL 9, Rocky 9, Ubuntu LTS)
- Historical trend visualisations (sparkline compliance trajectories)
- Background job orchestration for long-running audits
- Role-based access control for shared operations teams

## License

The compliance engine retains its original Creative Commons BY-NC-SA 4.0 license. New code added for NovaShield is provided under the same terms for consistency.
