from __future__ import annotations

import json
from html import escape

from app.services.session_service import build_service


SERVICE = build_service()


def _status_class(verdict: str) -> str:
    return {
        "stable": "stable",
        "watch": "watch",
        "review": "review",
    }[verdict]


def _shell(title: str, subtitle: str, current: str, body: str) -> str:
    summary = SERVICE.summary()
    nav_items = [
        ("/", "Overview", "overview"),
        ("/sessions", "Sessions", "sessions"),
        ("/approvals", "Approvals", "approvals"),
        ("/replay", "Replay", "replay"),
        ("/docs", "Docs", "docs"),
    ]
    sidebar = "".join(
        f"""<a class="side-link {'active' if key == current else ''}" href="{href}">{escape(label)}</a>"""
        for href, label, key in nav_items
    )
    tabs = "".join(
        f"""<a class="tab-pill {'active' if key == current else ''}" href="{href}">{escape(label)}</a>"""
        for href, label, key in nav_items
    )
    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{escape(title)}</title>
    <style>
      :root {{
        color-scheme: dark;
        --bg: #06111f;
        --panel: rgba(8, 16, 31, 0.9);
        --panel-soft: rgba(255, 255, 255, 0.04);
        --line: rgba(126, 180, 255, 0.14);
        --text: #eef3fb;
        --muted: #95a8c4;
        --aqua: #7ad3ff;
        --blue: #548aff;
        --green: #53d7a2;
        --amber: #f4c76d;
        --red: #ff8a96;
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Inter, "Segoe UI", sans-serif;
        background:
          radial-gradient(circle at top left, rgba(84, 138, 255, 0.16), transparent 30%),
          radial-gradient(circle at top right, rgba(122, 211, 255, 0.12), transparent 28%),
          linear-gradient(180deg, #03101d 0%, var(--bg) 50%, #020914 100%);
        color: var(--text);
      }}
      a {{ color: inherit; text-decoration: none; }}
      .shell {{ min-height: 100vh; display: grid; grid-template-columns: 248px minmax(0, 1fr); }}
      .sidebar {{
        border-right: 1px solid rgba(255,255,255,0.06);
        background: rgba(0,0,0,0.24);
        backdrop-filter: blur(16px);
        padding: 24px 18px;
        display: flex;
        flex-direction: column;
        gap: 18px;
      }}
      .brand {{
        padding: 12px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
      }}
      .brand strong {{ display: block; font-size: 14px; }}
      .brand span {{
        display: block;
        margin-top: 6px;
        color: var(--aqua);
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .side-link {{
        padding: 13px 14px;
        border-radius: 14px;
        color: #7f93b2;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
      }}
      .side-link.active {{
        color: var(--aqua);
        background: rgba(122, 211, 255, 0.08);
        border: 1px solid rgba(122, 211, 255, 0.16);
      }}
      .side-meta {{
        margin-top: auto;
        padding: 14px 12px 4px;
        border-top: 1px solid rgba(255,255,255,0.06);
      }}
      .side-meta div {{ margin-bottom: 12px; }}
      .side-meta small {{
        display: block;
        color: #667a97;
        font-size: 10px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
      }}
      .side-meta strong {{ display: block; margin-top: 4px; font-size: 13px; }}
      .main {{ min-width: 0; }}
      .topbar {{
        position: sticky;
        top: 0;
        z-index: 2;
        height: 72px;
        padding: 0 34px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        background: rgba(0,0,0,0.28);
        backdrop-filter: blur(16px);
      }}
      .status-chip {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 9px 14px;
        border-radius: 999px;
        color: #c9ecff;
        background: rgba(122,211,255,0.08);
        border: 1px solid rgba(122,211,255,0.16);
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: var(--aqua);
        box-shadow: 0 0 16px rgba(122,211,255,0.8);
      }}
      .wrap {{ max-width: 1280px; margin: 0 auto; padding: 34px; }}
      .hero {{
        padding: 28px;
        border-radius: 28px;
        border: 1px solid var(--line);
        background:
          radial-gradient(circle at top right, rgba(84,138,255,0.18), transparent 34%),
          linear-gradient(180deg, rgba(8,16,31,0.98), rgba(5,11,22,0.94));
        box-shadow: 0 24px 64px rgba(0,0,0,0.28);
      }}
      .hero-eyebrow {{
        color: var(--aqua);
        font-size: 11px;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      h1 {{
        margin: 14px 0 0;
        font-size: clamp(40px, 5vw, 72px);
        line-height: 0.92;
        font-family: Georgia, "Times New Roman", serif;
        letter-spacing: -0.04em;
      }}
      .hero-subtitle {{
        max-width: 820px;
        margin-top: 14px;
        color: var(--muted);
        font-size: 19px;
        line-height: 1.55;
      }}
      .hero-kpis {{
        margin-top: 24px;
        display: grid;
        gap: 14px;
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }}
      .hero-kpi {{
        padding: 16px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.03);
      }}
      .hero-kpi .k {{
        color: #6f83a0;
        font-size: 10px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 800;
      }}
      .hero-kpi .v {{
        margin-top: 8px;
        font-size: 28px;
        font-weight: 900;
      }}
      .hero-callout {{
        margin-top: 18px;
        padding: 18px 20px;
        border-radius: 18px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
      }}
      .hero-callout strong {{
        display: block;
        margin-bottom: 8px;
        color: var(--aqua);
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .hero-callout p {{ margin: 0; font-size: 17px; line-height: 1.5; color: #d9e8fb; }}
      .tab-row {{ display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }}
      .tab-pill {{
        padding: 10px 14px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        color: #afc2dd;
        background: rgba(255,255,255,0.03);
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      .tab-pill.active {{
        color: var(--aqua);
        background: rgba(122,211,255,0.08);
        border-color: rgba(122,211,255,0.16);
      }}
      .section {{
        margin-top: 24px;
        border: 1px solid var(--line);
        border-radius: 26px;
        background: var(--panel);
        overflow: hidden;
      }}
      .section-head {{
        padding: 20px 24px 14px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
      }}
      .section-head strong {{
        display: block;
        margin-bottom: 10px;
        color: var(--aqua);
        font-size: 10px;
        letter-spacing: 0.2em;
        text-transform: uppercase;
      }}
      .section-head h2 {{
        margin: 0;
        font-size: 24px;
        font-family: Georgia, "Times New Roman", serif;
        letter-spacing: -0.03em;
      }}
      .section-head p {{
        margin: 10px 0 0;
        color: var(--muted);
        font-size: 15px;
        line-height: 1.55;
      }}
      .section-body {{ padding: 24px; }}
      .grid-4 {{ display: grid; gap: 18px; grid-template-columns: repeat(4, minmax(0, 1fr)); }}
      .card {{
        padding: 18px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.03);
      }}
      .card .label {{
        color: #71839d;
        font-size: 10px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 800;
      }}
      .card .value {{ margin-top: 10px; font-size: 36px; font-weight: 900; }}
      .card .sub {{ margin-top: 10px; color: var(--muted); font-size: 14px; line-height: 1.5; }}
      .columns {{ display: grid; gap: 18px; grid-template-columns: 1.2fr 1fr; }}
      .panel {{
        padding: 20px;
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(4,10,20,0.64);
      }}
      .panel h3 {{ margin: 0 0 14px; font-size: 18px; }}
      .mini-list {{ display: grid; gap: 14px; }}
      .mini {{
        padding: 14px;
        border-radius: 16px;
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.05);
      }}
      .mini .micro {{
        color: #6f83a0;
        font-size: 9px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .mini .title {{ margin-top: 8px; font-size: 15px; font-weight: 800; }}
      .mini .desc {{ margin-top: 8px; color: var(--muted); font-size: 13px; line-height: 1.5; }}
      .session-grid {{ display: grid; gap: 16px; }}
      .session-card {{
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(4,10,20,0.62);
        overflow: hidden;
      }}
      .session-top {{
        padding: 20px 22px;
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto auto;
        gap: 18px;
        align-items: center;
      }}
      .session-top h3 {{ margin: 0; font-size: 22px; letter-spacing: -0.03em; }}
      .meta {{ margin-top: 8px; color: var(--muted); font-size: 13px; }}
      .tag {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 12px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
      }}
      .stable {{ color: var(--green); background: rgba(83,215,162,0.12); border: 1px solid rgba(83,215,162,0.16); }}
      .watch {{ color: var(--amber); background: rgba(244,199,109,0.12); border: 1px solid rgba(244,199,109,0.16); }}
      .review {{ color: var(--red); background: rgba(255,138,150,0.12); border: 1px solid rgba(255,138,150,0.16); }}
      .score-stack {{ text-align: right; }}
      .score-stack .micro {{
        color: #6f83a0;
        font-size: 9px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .score-stack .value {{ margin-top: 6px; font-size: 28px; font-weight: 900; }}
      .session-bottom {{
        padding: 18px 22px 22px;
        border-top: 1px solid rgba(255,255,255,0.05);
        background: rgba(255,255,255,0.02);
      }}
      .split {{ display: grid; gap: 16px; grid-template-columns: 1fr 1fr; }}
      .pill-row {{ display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }}
      .pill {{
        display: inline-flex;
        align-items: center;
        padding: 7px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        color: #d6e6fb;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }}
      .table-shell {{
        overflow: hidden;
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(4,10,20,0.6);
      }}
      table {{ width: 100%; border-collapse: collapse; }}
      th, td {{ padding: 16px 18px; text-align: left; vertical-align: top; }}
      thead th {{
        color: #7385a0;
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        background: rgba(255,255,255,0.04);
      }}
      tbody tr + tr td {{ border-top: 1px solid rgba(255,255,255,0.05); }}
      .subtext {{ margin-top: 6px; color: var(--muted); font-size: 12px; line-height: 1.45; }}
      pre {{
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
        color: #dce9ff;
        font: 13px/1.55 "Cascadia Code", Consolas, monospace;
      }}
      .footer {{
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        margin-top: 18px;
        padding: 12px 4px 0;
        color: #7c90ae;
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      @media (max-width: 1100px) {{
        .shell {{ grid-template-columns: 1fr; }}
        .sidebar {{ display: none; }}
        .hero-kpis, .grid-4, .columns, .split {{ grid-template-columns: 1fr; }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <aside class="sidebar">
        <div class="brand">
          <strong>MCP Session Recorder</strong>
          <span>Replay-ready governance</span>
        </div>
        {sidebar}
        <div class="side-meta">
          <div><small>Active sessions</small><strong>{summary["sessionCount"]}</strong></div>
          <div><small>Review pressure</small><strong>{summary["reviewSessions"]}</strong></div>
          <div><small>Evidence average</small><strong>{summary["averageEvidenceCoverage"]}%</strong></div>
        </div>
      </aside>
      <main class="main">
        <div class="topbar">
          <div class="status-chip"><span class="status-dot"></span>Evidence capture online</div>
          <div class="status-chip">Replay + approvals + audit trail</div>
        </div>
        <div class="wrap">
          <section class="hero">
            <div class="hero-eyebrow">MCP Session Recorder</div>
            <h1>{escape(title)}</h1>
            <div class="hero-subtitle">{escape(subtitle)}</div>
            <div class="hero-kpis">
              <div class="hero-kpi"><div class="k">Sessions</div><div class="v">{summary["sessionCount"]}</div></div>
              <div class="hero-kpi"><div class="k">Review sessions</div><div class="v">{summary["reviewSessions"]}</div></div>
              <div class="hero-kpi"><div class="k">Destructive calls</div><div class="v">{summary["destructiveToolCalls"]}</div></div>
              <div class="hero-kpi"><div class="k">Avg evidence</div><div class="v">{summary["averageEvidenceCoverage"]}%</div></div>
            </div>
            <div class="hero-callout">
              <strong>Lead recommendation</strong>
              <p>{escape(summary["leadRecommendation"])}</p>
            </div>
            <div class="tab-row">{tabs}</div>
          </section>
          {body}
          <div class="footer">
            <span>Protocol: MCP-R-2026</span>
            <span>Design: operator-first</span>
            <span>Surface: approval-aware</span>
            <span>Output: replayable evidence</span>
          </div>
        </div>
      </main>
    </div>
  </body>
</html>"""


def render_overview() -> str:
    summary = SERVICE.summary()
    sessions = SERVICE.sessions_board()
    body = f"""
      <section class="section">
        <div class="section-head">
          <strong>Control surface</strong>
          <h2>Session replay, approval history, and evidence posture in one place.</h2>
          <p>The recorder treats MCP usage like an operational event stream, not just a log file. That means every risky session keeps its tool path, approval path, and evidence chain attached.</p>
        </div>
        <div class="section-body">
          <div class="grid-4">
            <div class="card"><div class="label">Review pressure</div><div class="value">{summary["reviewSessions"]}</div><div class="sub">Sessions that still need direct containment, escalation, or approval repair.</div></div>
            <div class="card"><div class="label">Watch lane</div><div class="value">{summary["watchSessions"]}</div><div class="sub">Sessions that are still usable, but are building governance debt.</div></div>
            <div class="card"><div class="label">Citation average</div><div class="value">{summary["averageCitationCoverage"]}%</div><div class="sub">How often outputs stayed grounded in recorded evidence instead of unsupported action.</div></div>
            <div class="card"><div class="label">Approval required</div><div class="value">{summary["approvalRequiredSessions"]}</div><div class="sub">Sessions that invoked controls serious enough to force human signoff.</div></div>
          </div>
          <div class="columns" style="margin-top: 20px;">
            <div class="panel">
              <h3>Priority recorder lanes</h3>
              <div class="mini-list">
                <div class="mini"><div class="micro">Contain first</div><div class="title">Growth Ops MCP still has a broken destructive path.</div><div class="desc">The recorder captured an unsigned destructive request, incomplete citation coverage, and an open security escalation in the same session.</div></div>
                <div class="mini"><div class="micro">Reference baseline</div><div class="title">Support Copilot is the clean replay lane.</div><div class="desc">No destructive calls, strong evidence coverage, and deterministic replay markers make it the safest template for future MCP rollout.</div></div>
                <div class="mini"><div class="micro">What to tighten next</div><div class="title">Policy mutations still need deeper source binding.</div><div class="desc">Analytics and finance sessions are good enough to ship, but still too thin to survive a strict post-incident or audit review.</div></div>
              </div>
            </div>
            <div class="panel">
              <h3>Top session snapshot</h3>
              <div class="mini-list">
                <div class="mini"><div class="micro">Server</div><div class="title">{escape(sessions[0]["serverName"])}</div><div class="desc">{escape(sessions[0]["operator"])} · {escape(sessions[0]["environment"])} · {escape(sessions[0]["authModel"])}</div></div>
                <div class="mini"><div class="micro">Next action</div><div class="title">{escape(sessions[0]["nextAction"])}</div><div class="desc">Replayability only matters if the output also leads to an operator decision about what to freeze, inspect, or improve next.</div></div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <strong>Session board</strong>
          <h2>The highest-risk runs stay visible.</h2>
          <p>Sessions are ranked by replay pressure, destructive exposure, and what would matter in a real review queue.</p>
        </div>
        <div class="section-body">
          <div class="session-grid">
            {"".join(_session_card(session) for session in sessions)}
          </div>
        </div>
      </section>
    """
    return _shell(
        "Capture every MCP session as evidence, not just activity.",
        "Replayable operator history for tool calls, human approvals, citation coverage, and post-incident review pressure.",
        "overview",
        body,
    )


def _session_card(session: dict) -> str:
    tools = "".join(f'<span class="pill">{escape(tool["name"])}</span>' for tool in session["toolCalls"])
    trail = "".join(
        f'<div class="mini"><div class="micro">Evidence note</div><div class="desc">{escape(note)}</div></div>'
        for note in session["evidenceTrail"][:2]
    )
    return f"""
      <div class="session-card">
        <div class="session-top">
          <div>
            <h3>{escape(session["serverName"])}</h3>
            <div class="meta">{escape(session["sessionId"])} · {escape(session["operator"])} · {escape(session["environment"])} · {escape(session["authModel"])}</div>
          </div>
          <span class="tag {_status_class(session["verdict"])}">{escape(session["verdict"])}</span>
          <div class="score-stack"><div class="micro">Risk score</div><div class="value">{session["riskScore"]}</div></div>
        </div>
        <div class="session-bottom">
          <div class="split">
            <div>
              <div class="mini"><div class="micro">Next action</div><div class="title">{escape(session["nextAction"])}</div><div class="desc">Approval status: {escape(session["humanApproval"])} · evidence {session["evidenceCoverage"]}% · citations {session["citationCoverage"]}%</div></div>
              <div class="pill-row">{tools}</div>
            </div>
            <div class="mini-list">
              {trail}
            </div>
          </div>
        </div>
      </div>
    """


def render_sessions() -> str:
    rows = "".join(
        f"""
        <tr>
          <td><strong>{escape(session["sessionId"])}</strong><div class="subtext">{escape(session["serverName"])} · {escape(session["operator"])}</div></td>
          <td><span class="tag {_status_class(session["verdict"])}">{escape(session["verdict"])}</span></td>
          <td>{session["riskScore"]}</td>
          <td>{session["evidenceCoverage"]}%</td>
          <td>{session["citationCoverage"]}%</td>
          <td><div>{escape(session["humanApproval"])}</div><div class="subtext">{session["approvalLatencyMinutes"]} min latency</div></td>
        </tr>
        """
        for session in SERVICE.sessions_board()
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <strong>Session index</strong>
          <h2>Every run keeps its replay posture attached.</h2>
          <p>The recorder is useful because it keeps approval latency, evidence coverage, and session identity together instead of splitting them across three systems.</p>
        </div>
        <div class="section-body">
          <div class="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Session identity</th>
                  <th>Verdict</th>
                  <th>Risk</th>
                  <th>Evidence</th>
                  <th>Citations</th>
                  <th>Approval lane</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>
      </section>
    """
    return _shell(
        "Session board for operator replay pressure.",
        "Session-level posture across risk, evidence, citation coverage, and approval latency.",
        "sessions",
        body,
    )


def render_approvals() -> str:
    rows = "".join(
        f"""
        <tr>
          <td><strong>{escape(row["step"])}</strong><div class="subtext">{escape(row["sessionId"])} · {escape(row["serverName"])}</div></td>
          <td>{escape(row["owner"])}</td>
          <td><span class="tag {'review' if row['status'] == 'open' else 'stable'}">{escape(row["status"])}</span></td>
          <td>{escape(row["timestamp"])}</td>
          <td>{row["riskScore"]}</td>
        </tr>
        """
        for row in SERVICE.approval_board()
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <strong>Approval chain</strong>
          <h2>Human signoff stops being hand-wavy.</h2>
          <p>Approval is only useful if we can prove who touched the session, when they touched it, and whether the evidence trail stayed intact after that decision.</p>
        </div>
        <div class="section-body">
          <div class="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Review step</th>
                  <th>Owner</th>
                  <th>Status</th>
                  <th>Timestamp</th>
                  <th>Risk score</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>
      </section>
    """
    return _shell(
        "Approval board for MCP session review.",
        "Every human approval, escalation, and open exception remains attached to the recorded session path.",
        "approvals",
        body,
    )


def render_replay() -> str:
    payload = json.dumps(SERVICE.sample_payload(), indent=2)
    rows = "".join(
        f"""
        <div class="mini">
          <div class="micro">{escape(item["sessionId"])}</div>
          <div class="title">{escape(item["serverName"])} · {item["artifactCount"]} artifacts</div>
          <div class="desc">{escape(item["nextAction"])} Missing citations: {item["missingCitations"]}.</div>
        </div>
        """
        for item in SERVICE.replay_board()
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <strong>Replay methodology</strong>
          <h2>Record enough to explain the decision later.</h2>
          <p>The recorder is designed for the uncomfortable moment after an incident, when someone asks what the model did, what the operator approved, and what evidence was actually available at the time.</p>
        </div>
        <div class="section-body">
          <div class="columns">
            <div class="panel">
              <h3>Replay lanes</h3>
              <div class="mini-list">{rows}</div>
            </div>
            <div class="panel">
              <h3>Structured payload</h3>
              <pre>{escape(payload)}</pre>
            </div>
          </div>
        </div>
      </section>
    """
    return _shell(
        "Replay board for evidence chains and approval history.",
        "Structured outputs for session replay, evidence completeness, and operator review workflows.",
        "replay",
        body,
    )


def render_docs() -> str:
    body = """
      <section class="section">
        <div class="section-head">
          <strong>Implementation notes</strong>
          <h2>What the recorder actually ships.</h2>
          <p>This repo uses a FastAPI surface, sample session inventory, replay scoring, approval tracking, and static SVG proof generation from the same service state.</p>
        </div>
        <div class="section-body">
          <div class="columns">
            <div class="panel">
              <h3>Included surfaces</h3>
              <div class="mini-list">
                <div class="mini"><div class="micro">Overview</div><div class="desc">Control-plane summary for session counts, review pressure, destructive calls, and lead action.</div></div>
                <div class="mini"><div class="micro">Sessions</div><div class="desc">Session board with risk, evidence, citation coverage, and human approval state.</div></div>
                <div class="mini"><div class="micro">Approvals</div><div class="desc">Timeline of review steps, owners, status, and escalation state.</div></div>
                <div class="mini"><div class="micro">Replay</div><div class="desc">Evidence-oriented view of artifacts, citation gaps, and replayability.</div></div>
              </div>
            </div>
            <div class="panel">
              <h3>Design philosophy</h3>
              <div class="mini-list">
                <div class="mini"><div class="micro">Operator-first</div><div class="desc">The recorder answers what happened and what to do next, not just what was logged.</div></div>
                <div class="mini"><div class="micro">CI-native</div><div class="desc">JSON APIs and proof assets are shaped so this can feed tests, gates, or future MCP governance tooling.</div></div>
                <div class="mini"><div class="micro">CISO-legible</div><div class="desc">Human approvals, destructive paths, and evidence gaps stay visible without reading raw traces.</div></div>
              </div>
            </div>
          </div>
        </div>
      </section>
    """
    return _shell(
        "Recorder documentation surface.",
        "Implementation notes, design philosophy, and proof-layer intent for the MCP session recorder.",
        "docs",
        body,
    )
