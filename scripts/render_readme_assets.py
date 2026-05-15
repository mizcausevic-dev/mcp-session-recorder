from __future__ import annotations

import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.session_service import build_service


OUT_DIR = ROOT / "screenshots"
OUT_DIR.mkdir(exist_ok=True)

WIDTH = 1600
HEIGHT = 980
SERVICE = build_service()


def shell(title: str, subtitle: str, body: str) -> str:
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='{WIDTH}' height='{HEIGHT}' viewBox='0 0 {WIDTH} {HEIGHT}'>
  <defs>
    <linearGradient id='bg' x1='0' x2='0' y1='0' y2='1'>
      <stop offset='0%' stop-color='#03101d'/>
      <stop offset='100%' stop-color='#06111f'/>
    </linearGradient>
    <linearGradient id='hero' x1='0' x2='1' y1='0' y2='1'>
      <stop offset='0%' stop-color='#0b1729'/>
      <stop offset='100%' stop-color='#08121f'/>
    </linearGradient>
    <linearGradient id='blue' x1='0' x2='1' y1='0' y2='0'>
      <stop offset='0%' stop-color='#0fa2d7'/>
      <stop offset='100%' stop-color='#548aff'/>
    </linearGradient>
  </defs>
  <rect width='{WIDTH}' height='{HEIGHT}' fill='url(#bg)'/>
  <rect x='0' y='0' width='252' height='{HEIGHT}' fill='rgba(0,0,0,0.26)'/>
  <rect x='0' y='0' width='252' height='{HEIGHT}' fill='none' stroke='rgba(255,255,255,0.06)'/>
  <rect x='22' y='28' width='208' height='62' rx='18' fill='rgba(255,255,255,0.03)' stroke='rgba(255,255,255,0.08)'/>
  <text x='40' y='56' fill='#eef3fb' font-size='15' font-family='Segoe UI' font-weight='700'>MCP Session Recorder</text>
  <text x='40' y='76' fill='#7ad3ff' font-size='10' font-family='Segoe UI' letter-spacing='3'>REPLAY-READY GOVERNANCE</text>
  <text x='36' y='142' fill='#7ad3ff' font-size='11' font-family='Segoe UI' letter-spacing='4'>ACTIVE VIEWS</text>
  <rect x='26' y='164' width='198' height='42' rx='14' fill='rgba(122,211,255,0.08)' stroke='rgba(122,211,255,0.16)'/>
  <text x='42' y='190' fill='#7ad3ff' font-size='12' font-family='Segoe UI' letter-spacing='2'>OVERVIEW</text>
  <text x='42' y='236' fill='#7f93b2' font-size='12' font-family='Segoe UI' letter-spacing='2'>SESSIONS</text>
  <text x='42' y='282' fill='#7f93b2' font-size='12' font-family='Segoe UI' letter-spacing='2'>APPROVALS</text>
  <text x='42' y='328' fill='#7f93b2' font-size='12' font-family='Segoe UI' letter-spacing='2'>REPLAY</text>
  <rect x='252' y='0' width='{WIDTH - 252}' height='72' fill='rgba(0,0,0,0.28)'/>
  <rect x='286' y='20' width='220' height='30' rx='15' fill='rgba(122,211,255,0.08)' stroke='rgba(122,211,255,0.16)'/>
  <circle cx='306' cy='35' r='5' fill='#7ad3ff'/>
  <text x='322' y='39' fill='#c9ecff' font-size='10' font-family='Segoe UI' letter-spacing='3'>EVIDENCE CAPTURE ONLINE</text>
  <rect x='288' y='104' width='1248' height='248' rx='28' fill='url(#hero)' stroke='rgba(126,180,255,0.16)'/>
  <text x='324' y='146' fill='#7ad3ff' font-size='11' font-family='Segoe UI' letter-spacing='5'>MCP SESSION RECORDER</text>
  <text x='324' y='210' fill='#eef3fb' font-size='42' font-family='Georgia' font-weight='700'>{escape(title)}</text>
  <text x='324' y='246' fill='#95a8c4' font-size='21' font-family='Segoe UI'>{escape(subtitle)}</text>
  {body}
</svg>"""


def overview_svg() -> str:
    summary = SERVICE.summary()
    body = f"""
  <rect x='324' y='274' width='284' height='126' rx='20' fill='rgba(255,255,255,0.04)' stroke='rgba(255,255,255,0.06)'/>
  <text x='348' y='302' fill='#71839d' font-size='10' font-family='Segoe UI' letter-spacing='3'>REVIEW SESSIONS</text>
  <text x='348' y='350' fill='#eef3fb' font-size='40' font-family='Segoe UI' font-weight='700'>{summary["reviewSessions"]}</text>
  <text x='348' y='382' fill='#95a8c4' font-size='14' font-family='Segoe UI'>Runs that still need containment or approval repair.</text>
  <rect x='626' y='274' width='284' height='126' rx='20' fill='rgba(255,255,255,0.04)' stroke='rgba(255,255,255,0.06)'/>
  <text x='650' y='302' fill='#71839d' font-size='10' font-family='Segoe UI' letter-spacing='3'>WATCH SESSIONS</text>
  <text x='650' y='350' fill='#eef3fb' font-size='40' font-family='Segoe UI' font-weight='700'>{summary["watchSessions"]}</text>
  <text x='650' y='382' fill='#95a8c4' font-size='14' font-family='Segoe UI'>Useful sessions that are still accumulating governance debt.</text>
  <rect x='928' y='274' width='284' height='126' rx='20' fill='rgba(255,255,255,0.04)' stroke='rgba(255,255,255,0.06)'/>
  <text x='952' y='302' fill='#71839d' font-size='10' font-family='Segoe UI' letter-spacing='3'>DESTRUCTIVE CALLS</text>
  <text x='952' y='350' fill='#eef3fb' font-size='40' font-family='Segoe UI' font-weight='700'>{summary["destructiveToolCalls"]}</text>
  <text x='952' y='382' fill='#95a8c4' font-size='14' font-family='Segoe UI'>State-changing actions captured with replay pressure.</text>
  <rect x='1230' y='274' width='284' height='126' rx='20' fill='rgba(255,255,255,0.04)' stroke='rgba(255,255,255,0.06)'/>
  <text x='1254' y='302' fill='#71839d' font-size='10' font-family='Segoe UI' letter-spacing='3'>AVG EVIDENCE</text>
  <text x='1254' y='350' fill='#eef3fb' font-size='40' font-family='Segoe UI' font-weight='700'>{summary["averageEvidenceCoverage"]}%</text>
  <text x='1254' y='382' fill='#95a8c4' font-size='14' font-family='Segoe UI'>Cross-session evidence completeness and artifact quality.</text>
  <rect x='324' y='418' width='1190' height='82' rx='18' fill='rgba(255,255,255,0.03)' stroke='rgba(255,255,255,0.06)'/>
  <text x='350' y='448' fill='#7ad3ff' font-size='10' font-family='Segoe UI' letter-spacing='3'>LEAD RECOMMENDATION</text>
  <text x='350' y='480' fill='#dce9fb' font-size='18' font-family='Segoe UI'>{escape(summary["leadRecommendation"])}</text>
  <rect x='324' y='526' width='1190' height='344' rx='22' fill='rgba(4,10,20,0.62)' stroke='rgba(255,255,255,0.06)'/>
  <text x='350' y='560' fill='#eef3fb' font-size='22' font-family='Georgia' font-weight='700'>Priority session board</text>
  {_session_rows()}
    """
    return shell("Capture every MCP session as evidence, not just activity.", "Replayable history for tool calls, approvals, citations, and post-incident review pressure.", body)


def _session_rows() -> str:
    rows = []
    y = 592
    for session in SERVICE.sessions_board()[:3]:
        tone = {"stable": "#53d7a2", "watch": "#f4c76d", "review": "#ff8a96"}[session["verdict"]]
        rows.append(
            f"""
  <rect x='350' y='{y}' width='1138' height='82' rx='18' fill='rgba(255,255,255,0.03)' stroke='rgba(255,255,255,0.05)'/>
  <text x='374' y='{y + 28}' fill='#eef3fb' font-size='20' font-family='Segoe UI' font-weight='700'>{escape(session["serverName"])}</text>
  <text x='374' y='{y + 50}' fill='#95a8c4' font-size='12' font-family='Segoe UI'>{escape(session["sessionId"])} · {escape(session["operator"])} · {escape(session["authModel"])}</text>
  <text x='1180' y='{y + 28}' fill='{tone}' font-size='11' font-family='Segoe UI' font-weight='700' letter-spacing='2'>{escape(session["verdict"].upper())}</text>
  <text x='1388' y='{y + 28}' fill='#71839d' font-size='10' font-family='Segoe UI' letter-spacing='2'>RISK</text>
  <text x='1468' y='{y + 32}' fill='#eef3fb' font-size='28' font-family='Segoe UI' font-weight='700'>{session["riskScore"]}</text>
  <text x='374' y='{y + 70}' fill='#dce9fb' font-size='12' font-family='Segoe UI'>{escape(session["nextAction"][:120])}</text>
            """
        )
        y += 98
    return "".join(rows)


def sessions_svg() -> str:
    rows = []
    y = 536
    for session in SERVICE.sessions_board():
        rows.append(
            f"""
  <rect x='350' y='{y}' width='1140' height='58' fill='{"rgba(255,255,255,0.025)" if ((y // 58) % 2) else "rgba(0,0,0,0.06)"}'/>
  <text x='374' y='{y + 24}' fill='#eef3fb' font-size='14' font-family='Segoe UI' font-weight='700'>{escape(session["sessionId"])}</text>
  <text x='374' y='{y + 42}' fill='#95a8c4' font-size='11' font-family='Segoe UI'>{escape(session["serverName"])} · {escape(session["operator"])}</text>
  <text x='760' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{session["riskScore"]}</text>
  <text x='890' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{session["evidenceCoverage"]}%</text>
  <text x='1040' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{session["citationCoverage"]}%</text>
  <text x='1210' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{escape(session["humanApproval"])}</text>
  <text x='1412' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{session["approvalLatencyMinutes"]}m</text>
            """
        )
        y += 58
    body = f"""
  <rect x='324' y='420' width='1190' height='450' rx='22' fill='rgba(4,10,20,0.62)' stroke='rgba(255,255,255,0.06)'/>
  <text x='350' y='454' fill='#7ad3ff' font-size='10' font-family='Segoe UI' letter-spacing='3'>SESSION INDEX</text>
  <text x='350' y='490' fill='#eef3fb' font-size='24' font-family='Georgia' font-weight='700'>Every run keeps its replay posture attached.</text>
  <rect x='350' y='510' width='1140' height='28' fill='rgba(255,255,255,0.04)'/>
  <text x='374' y='528' fill='#7385a0' font-size='10' font-family='Segoe UI' font-weight='700' letter-spacing='3'>SESSION IDENTITY</text>
  <text x='760' y='528' fill='#7385a0' font-size='10' font-family='Segoe UI' font-weight='700' letter-spacing='3'>RISK</text>
  <text x='890' y='528' fill='#7385a0' font-size='10' font-family='Segoe UI' font-weight='700' letter-spacing='3'>EVIDENCE</text>
  <text x='1040' y='528' fill='#7385a0' font-size='10' font-family='Segoe UI' font-weight='700' letter-spacing='3'>CITATIONS</text>
  <text x='1210' y='528' fill='#7385a0' font-size='10' font-family='Segoe UI' font-weight='700' letter-spacing='3'>APPROVAL</text>
  <text x='1412' y='528' fill='#7385a0' font-size='10' font-family='Segoe UI' font-weight='700' letter-spacing='3'>LATENCY</text>
  {"".join(rows)}
    """
    return shell("Session board for operator replay pressure.", "Session-level posture across risk, evidence, citations, and approval latency.", body)


def approvals_svg() -> str:
    rows = []
    y = 540
    for row in SERVICE.approval_board():
        tone = "#ff8a96" if row["status"] == "open" else "#53d7a2"
        rows.append(
            f"""
  <rect x='350' y='{y}' width='1140' height='62' rx='16' fill='rgba(255,255,255,0.03)' stroke='rgba(255,255,255,0.05)'/>
  <text x='374' y='{y + 26}' fill='#eef3fb' font-size='14' font-family='Segoe UI' font-weight='700'>{escape(row["step"])}</text>
  <text x='374' y='{y + 46}' fill='#95a8c4' font-size='11' font-family='Segoe UI'>{escape(row["sessionId"])} · {escape(row["serverName"])}</text>
  <text x='900' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{escape(row["owner"])}</text>
  <text x='1128' y='{y + 34}' fill='{tone}' font-size='11' font-family='Segoe UI' font-weight='700' letter-spacing='2'>{escape(row["status"].upper())}</text>
  <text x='1300' y='{y + 34}' fill='#eef3fb' font-size='12' font-family='Segoe UI'>{row["riskScore"]}</text>
            """
        )
        y += 78
    body = f"""
  <rect x='324' y='420' width='1190' height='450' rx='22' fill='rgba(4,10,20,0.62)' stroke='rgba(255,255,255,0.06)'/>
  <text x='350' y='454' fill='#7ad3ff' font-size='10' font-family='Segoe UI' letter-spacing='3'>APPROVAL BOARD</text>
  <text x='350' y='490' fill='#eef3fb' font-size='24' font-family='Georgia' font-weight='700'>Human signoff stays attached to the session.</text>
  {"".join(rows)}
    """
    return shell("Approval board for MCP session review.", "Every review step, owner, and open escalation remains attached to the recorded run.", body)


def replay_svg() -> str:
    payload = json.dumps(SERVICE.sample_payload(), indent=2)
    body = f"""
  <rect x='324' y='420' width='570' height='450' rx='22' fill='rgba(4,10,20,0.62)' stroke='rgba(255,255,255,0.06)'/>
  <text x='350' y='454' fill='#7ad3ff' font-size='10' font-family='Segoe UI' letter-spacing='3'>REPLAY METHODOLOGY</text>
  <text x='350' y='490' fill='#eef3fb' font-size='24' font-family='Georgia' font-weight='700'>Record enough to explain the decision later.</text>
  <text x='350' y='534' fill='#dce9fb' font-size='14' font-family='Segoe UI'>1. Capture tool path and operator identity</text>
  <text x='350' y='568' fill='#dce9fb' font-size='14' font-family='Segoe UI'>2. Preserve human approval chain when it exists</text>
  <text x='350' y='602' fill='#dce9fb' font-size='14' font-family='Segoe UI'>3. Count evidence artifacts and citation gaps</text>
  <text x='350' y='636' fill='#dce9fb' font-size='14' font-family='Segoe UI'>4. Keep a replay-ready next action with the record</text>
  <rect x='920' y='420' width='594' height='450' rx='22' fill='rgba(2,7,14,0.92)' stroke='rgba(255,255,255,0.08)'/>
  <text x='946' y='454' fill='#7ad3ff' font-size='10' font-family='Segoe UI' letter-spacing='3'>/API/SAMPLE</text>
  <foreignObject x='946' y='476' width='540' height='360'>
    <div xmlns='http://www.w3.org/1999/xhtml' style='color:#dce9ff;font:13px/1.55 Consolas,monospace;white-space:pre-wrap'>{escape(payload)}</div>
  </foreignObject>
    """
    return shell("Replay board for evidence chains and approval history.", "Structured outputs for post-incident review, evidence completeness, and operator audit posture.", body)


def main() -> None:
    for path in OUT_DIR.iterdir():
        if path.is_file():
            path.unlink()
    (OUT_DIR / "01-overview.svg").write_text(overview_svg(), encoding="utf-8")
    (OUT_DIR / "02-sessions.svg").write_text(sessions_svg(), encoding="utf-8")
    (OUT_DIR / "03-approvals.svg").write_text(approvals_svg(), encoding="utf-8")
    (OUT_DIR / "04-replay.svg").write_text(replay_svg(), encoding="utf-8")
    print("rendered screenshots")


if __name__ == "__main__":
    main()
