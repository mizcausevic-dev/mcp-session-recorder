# Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-05-15

### Released
- Published **mcp-session-recorder** as a public Python and FastAPI service for replayable MCP session history, approval tracking, evidence chains, and audit-facing review posture.
- Packaged HTML proof surfaces, JSON APIs, generated SVG screenshots, validation scripts, CI, and narrative documentation into a public repo.
- Positioned the project around a specific governance gap: teams can often log tool usage, but still cannot reconstruct the operator decision path cleanly after a risky session.

### Why this mattered
- Existing logging, tracing, and policy tooling usually answer only part of the session-review problem.
- What remained missing was a recorder that kept tool path, human approval, citation coverage, and next action visible in one surface.
- This release made the repo read like a real operator capability instead of a generic MCP demo.

## [0.1.0] - 2026-02-27

### Shipped
- Cut the first coherent internal version of the recorder with stable session objects, approval timelines, and replay prioritization logic.
- Locked the architecture around the core promise: Python FastAPI recorder for MCP session replay, approval history, evidence chains, and operator-facing audit posture.
- Chose to keep the product intentionally small and review-focused instead of turning it into another broad observability wrapper.

## [Prototype] - 2025-08-12

### Built
- Built the first runnable prototype for capturing MCP session identity, tool calls, evidence artifacts, and approval state in a single record.
- Tested whether a session-oriented surface was more useful than raw logs when reviewing destructive or state-changing actions.
- Validated the idea against recurring enterprise concerns like incomplete approval evidence, prompt-driven action ambiguity, and weak replayability.

## [Design Phase] - 2024-11-06

### Designed
- Defined the recorder around operator review instead of generic telemetry.
- Chose session objects, approval trails, and evidence notes as the primary building blocks.
- Kept the intended audience clear: platform leads, AI governance teams, and security reviewers who need legible answers fast.

## [Idea Origin] - 2023-06-19

### Observed
- The original idea surfaced while looking at how teams explained risky AI-assisted actions after the fact.
- The recurring problem was not a total absence of data. It was fragmented data across logs, tickets, chat, and policy documents with no clear replayable session boundary.

## [Background Signals] - 2022-09-08

### Context
- Earlier work in governance, access review, and operator tooling made one pattern obvious: the hardest systems to review are often the ones with partial controls and scattered evidence, not the ones with no controls at all.
- That pattern shaped the thinking behind this repo well before the public version existed.
