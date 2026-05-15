# Architecture

## Goal

`mcp-session-recorder` is a Python and FastAPI service for recording **how MCP sessions actually unfolded**, not just whether they happened.

The design centers on the post-execution questions that matter to operators, governance teams, and security reviewers:

- which server and operator initiated the session
- which tool calls were destructive or state-changing
- whether human approval happened and how long it took
- how much evidence and citation coverage survived the run
- which sessions should be replayed first when review pressure rises

## Service shape

The repo is intentionally compact and local-first:

- `app/main.py` exposes HTML proof routes and JSON APIs.
- `app/services/session_service.py` loads sample session records, approval steps, evidence trails, and recollection logic.
- `app/render.py` turns the same recorder state into a control-plane style HTML surface.
- `scripts/run_demo.py` and `scripts/smoke_check.py` provide one-shot validation paths.
- `scripts/render_readme_assets.py` generates the SVG proof assets used by the README.

## Recorder model

Each session keeps the fields an operator or reviewer would actually need later:

- session identity
- server identity and owner
- owner email and session visibility
- shared-with collaborator lanes
- operator identity
- auth model and environment
- risk score and verdict
- human approval state and latency
- evidence coverage
- citation coverage
- tool call inventory
- evidence trail notes
- next action

The point is not to preserve every possible trace detail. The point is to preserve enough structured context to support replay, approval review, and escalation decisions.

## Output lanes

The current proof surface exposes four main lanes:

- `overview` for control-plane summary
- `sessions` for ranked session inventory
- `approvals` for human signoff and escalation history
- `replay` for evidence completeness and replay readiness

The replay lane now also includes:

- play and pause controls
- temporal seeking
- playback speed changes
- dynamic event filtering based on the current replay cursor

Those controls are intentionally client-side and local-first. They make the audit story visible without pretending this sample repo is already a cloud multi-user product.

## Why it matters

Many MCP examples stop at policy before execution or logs after execution.

Real operating teams need the bridge between those two:

- what happened
- who approved it
- what evidence was captured
- who else was allowed to view the session
- what still needs intervention

That is the layer this project is modeling.
