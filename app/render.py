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


def _severity_class(severity: str) -> str:
    return {
        "info": "tone-info",
        "stable": "tone-stable",
        "watch": "tone-watch",
        "review": "tone-review",
    }[severity]


def _shell(title: str, subtitle: str, current: str, body: str, page_script: str = "") -> str:
    summary = SERVICE.summary()
    nav_items = [
        ("/", "Audit Posture", "overview"),
        ("/sessions", "Session Inventory", "sessions"),
        ("/approvals", "Approval History", "approvals"),
        ("/replay", "Session Replay", "replay"),
        ("/docs", "Architecture", "docs"),
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
        --bg: #08090d;
        --bg-2: #0d1018;
        --panel: rgba(13, 16, 24, 0.94);
        --panel-soft: rgba(255, 255, 255, 0.03);
        --panel-strong: rgba(0, 0, 0, 0.3);
        --line: rgba(255, 255, 255, 0.07);
        --line-strong: rgba(255, 255, 255, 0.14);
        --text: #f6f7fb;
        --muted: #9ea5b6;
        --soft: #747c8e;
        --white: #ffffff;
        --green: #3ed598;
        --amber: #f4be55;
        --red: #ff5d73;
        --blue: #4f7cff;
        --blue-soft: #7eb0ff;
        --mono: "JetBrains Mono", "Cascadia Code", Consolas, monospace;
        --sans: "Inter", "Segoe UI", system-ui, sans-serif;
        --serif: Georgia, "Times New Roman", serif;
        --shadow: 0 28px 70px rgba(0, 0, 0, 0.38);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: var(--sans);
        color: var(--text);
        background:
          radial-gradient(circle at top right, rgba(79,124,255,0.12), transparent 24%),
          radial-gradient(circle at top left, rgba(255,255,255,0.04), transparent 18%),
          linear-gradient(180deg, #05070a 0%, var(--bg) 52%, #05070a 100%);
      }}
      a {{ color: inherit; text-decoration: none; }}
      .shell {{ min-height: 100vh; display: grid; grid-template-columns: 272px minmax(0, 1fr); }}
      .sidebar {{
        background: rgba(0,0,0,0.2);
        border-right: 1px solid rgba(255,255,255,0.06);
        padding: 24px 18px;
        display: flex;
        flex-direction: column;
        gap: 18px;
      }}
      .brand {{
        padding: 14px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.02);
      }}
      .brand-mark {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(135deg, #12151f, #090a0e);
        color: var(--white);
        font-size: 18px;
        font-weight: 900;
        margin-bottom: 12px;
      }}
      .brand strong {{
        display: block;
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -0.02em;
        text-transform: uppercase;
      }}
      .brand span {{
        display: block;
        margin-top: 6px;
        color: var(--soft);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .nav-label {{
        color: var(--soft);
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.24em;
        text-transform: uppercase;
        padding: 4px 10px 0;
      }}
      .side-link {{
        display: block;
        padding: 13px 14px;
        border-radius: 14px;
        color: #7f8798;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        transition: 160ms ease;
      }}
      .side-link:hover {{
        color: var(--text);
        background: rgba(255,255,255,0.03);
      }}
      .side-link.active {{
        color: var(--text);
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.02);
      }}
      .side-meta {{
        margin-top: auto;
        padding: 14px 12px 6px;
        border-top: 1px solid rgba(255,255,255,0.06);
      }}
      .side-meta .mini + .mini {{ margin-top: 12px; }}
      .side-meta .micro {{
        color: var(--soft);
        font-size: 10px;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        font-weight: 800;
      }}
      .side-meta .value {{
        margin-top: 4px;
        font-size: 14px;
        font-weight: 800;
      }}
      .main {{ min-width: 0; }}
      .topbar {{
        position: sticky;
        top: 0;
        z-index: 3;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        height: 68px;
        padding: 0 30px;
        background: rgba(0,0,0,0.28);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(18px);
      }}
      .status-chip {{
        display: inline-flex;
        align-items: center;
        gap: 10px;
        padding: 9px 14px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
        color: #d8dce7;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .status-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 14px rgba(62,213,152,0.8);
      }}
      .topbar-right {{
        display: flex;
        align-items: center;
        gap: 18px;
      }}
      .operator-id {{
        padding-right: 18px;
        border-right: 1px solid rgba(255,255,255,0.08);
        color: var(--soft);
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
      }}
      .operator-id strong {{
        display: block;
        margin-top: 5px;
        color: #d2d8e4;
        font-size: 11px;
      }}
      .terminate {{
        color: #acb2c3;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .terminate:hover {{ color: var(--red); }}
      .wrap {{ max-width: 1320px; margin: 0 auto; padding: 30px; }}
      .hero {{
        border-radius: 28px;
        border: 1px solid rgba(255,255,255,0.08);
        background:
          radial-gradient(circle at top right, rgba(79,124,255,0.14), transparent 28%),
          linear-gradient(180deg, #11151f 0%, #0a0d14 100%);
        box-shadow: var(--shadow);
        overflow: hidden;
      }}
      .hero-grid {{
        display: grid;
        gap: 26px;
        grid-template-columns: minmax(0, 1.3fr) 350px;
        padding: 28px;
      }}
      .eyebrow {{
        color: var(--soft);
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.26em;
        text-transform: uppercase;
      }}
      h1 {{
        margin: 14px 0 0;
        font-family: var(--serif);
        font-size: clamp(44px, 5vw, 76px);
        line-height: 0.9;
        letter-spacing: -0.05em;
      }}
      .hero-subtitle {{
        margin-top: 16px;
        max-width: 760px;
        color: var(--muted);
        font-size: 19px;
        line-height: 1.55;
      }}
      .hero-strip {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 22px;
      }}
      .tab-pill {{
        display: inline-flex;
        align-items: center;
        padding: 10px 13px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
        color: #c6cedd;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.14em;
        text-transform: uppercase;
      }}
      .tab-pill.active {{
        color: var(--white);
        border-color: rgba(255,255,255,0.14);
        background: rgba(255,255,255,0.06);
      }}
      .hero-side {{
        padding: 18px;
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.03);
      }}
      .hero-side .panel-label {{
        color: var(--soft);
        font-size: 10px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .hero-side .panel-title {{
        margin-top: 10px;
        font-size: 18px;
        font-weight: 800;
        line-height: 1.2;
      }}
      .hero-side .panel-copy {{
        margin-top: 10px;
        color: var(--muted);
        font-size: 14px;
        line-height: 1.55;
      }}
      .glow-row {{
        margin-top: 18px;
        display: grid;
        gap: 12px;
      }}
      .glow-item {{
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 11px;
        color: #dfe5f2;
      }}
      .glow-dot {{
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 18px rgba(62,213,152,0.8);
      }}
      .section {{
        margin-top: 24px;
        border-radius: 24px;
        border: 1px solid rgba(255,255,255,0.07);
        background: var(--panel);
        box-shadow: 0 22px 58px rgba(0,0,0,0.22);
        overflow: hidden;
      }}
      .section-head {{
        padding: 20px 24px 14px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
      }}
      .section-head .label {{
        color: var(--soft);
        font-size: 10px;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .section-head h2 {{
        margin: 10px 0 0;
        font-family: var(--serif);
        font-size: 26px;
        letter-spacing: -0.03em;
      }}
      .section-head p {{
        margin: 10px 0 0;
        color: var(--muted);
        font-size: 15px;
        line-height: 1.55;
      }}
      .section-body {{ padding: 24px; }}
      .stats-grid {{
        display: grid;
        gap: 16px;
        grid-template-columns: repeat(4, minmax(0, 1fr));
      }}
      .stat {{
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.025);
      }}
      .stat .micro {{
        color: var(--soft);
        font-size: 10px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .stat .value {{
        margin-top: 10px;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: -0.03em;
      }}
      .stat .copy {{
        margin-top: 10px;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.5;
      }}
      .columns {{
        display: grid;
        gap: 18px;
        grid-template-columns: 1.2fr 0.9fr;
      }}
      .panel {{
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.02);
      }}
      .panel h3 {{
        margin: 0 0 14px;
        font-size: 18px;
        font-weight: 800;
      }}
      .mini-list {{
        display: grid;
        gap: 14px;
      }}
      .mini {{
        padding: 14px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.05);
        background: rgba(0,0,0,0.16);
      }}
      .mini .micro {{
        color: var(--soft);
        font-size: 9px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .mini .title {{
        margin-top: 8px;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.3;
      }}
      .mini .desc {{
        margin-top: 8px;
        color: var(--muted);
        font-size: 13px;
        line-height: 1.55;
      }}
      .session-grid {{
        display: grid;
        gap: 16px;
      }}
      .session-card {{
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.02);
        overflow: hidden;
        transition: 180ms ease;
      }}
      .session-card:hover {{
        border-color: rgba(255,255,255,0.11);
        transform: translateY(-1px);
      }}
      .session-top {{
        display: grid;
        grid-template-columns: minmax(0, 1fr) auto auto;
        gap: 18px;
        align-items: center;
        padding: 20px 22px;
      }}
      .session-top h3 {{
        margin: 0;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.03em;
      }}
      .meta {{
        margin-top: 8px;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.5;
      }}
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
      .stable {{
        color: var(--green);
        background: rgba(62,213,152,0.12);
        border: 1px solid rgba(62,213,152,0.18);
      }}
      .watch {{
        color: var(--amber);
        background: rgba(244,190,85,0.12);
        border: 1px solid rgba(244,190,85,0.18);
      }}
      .review {{
        color: var(--red);
        background: rgba(255,93,115,0.12);
        border: 1px solid rgba(255,93,115,0.18);
        animation: pulse 2.2s infinite;
      }}
      .score-stack {{
        text-align: right;
      }}
      .score-stack .micro {{
        color: var(--soft);
        font-size: 9px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .score-stack .value {{
        margin-top: 6px;
        font-size: 28px;
        font-weight: 900;
      }}
      .session-bottom {{
        padding: 18px 22px 22px;
        border-top: 1px solid rgba(255,255,255,0.05);
        background: rgba(0,0,0,0.12);
      }}
      .split {{
        display: grid;
        gap: 16px;
        grid-template-columns: 1fr 1fr;
      }}
      .pill-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
      }}
      .pill {{
        display: inline-flex;
        align-items: center;
        padding: 6px 9px;
        border-radius: 999px;
        background: rgba(255,255,255,0.05);
        color: #d8deeb;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }}
      .table-shell {{
        overflow: hidden;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(0,0,0,0.15);
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        padding: 16px 18px;
        text-align: left;
        vertical-align: top;
      }}
      thead th {{
        color: var(--soft);
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        background: rgba(255,255,255,0.03);
      }}
      tbody tr + tr td {{
        border-top: 1px solid rgba(255,255,255,0.05);
      }}
      tbody tr:hover td {{
        background: rgba(255,255,255,0.02);
      }}
      .subtext {{
        margin-top: 6px;
        color: var(--muted);
        font-size: 12px;
        line-height: 1.45;
      }}
      .share-grid {{
        display: grid;
        gap: 16px;
        grid-template-columns: 1fr 0.95fr;
      }}
      .share-card {{
        padding: 18px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.02);
      }}
      .share-card .header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
      }}
      .share-card .header strong {{
        font-size: 16px;
      }}
      .share-list {{
        margin-top: 12px;
        display: grid;
        gap: 8px;
      }}
      .share-list div {{
        padding: 10px 12px;
        border-radius: 14px;
        background: rgba(0,0,0,0.18);
        color: #d8deeb;
        font-size: 12px;
        font-family: var(--mono);
      }}
      .share-button {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 11px 14px;
        border-radius: 12px;
        background: var(--white);
        color: #090a0e;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        cursor: pointer;
      }}
      .share-modal {{
        position: fixed;
        inset: 0;
        z-index: 6;
        display: none;
        align-items: center;
        justify-content: center;
        background: rgba(0,0,0,0.6);
        backdrop-filter: blur(10px);
      }}
      .share-modal.open {{ display: flex; }}
      .share-dialog {{
        width: min(520px, calc(100vw - 32px));
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.08);
        background: #0d1018;
        padding: 22px;
        box-shadow: 0 30px 70px rgba(0,0,0,0.5);
      }}
      .share-dialog h3 {{
        margin: 0;
        font-size: 22px;
        font-family: var(--serif);
      }}
      .share-dialog p {{
        margin: 10px 0 0;
        color: var(--muted);
        font-size: 14px;
        line-height: 1.55;
      }}
      .field {{
        margin-top: 18px;
      }}
      .field label {{
        display: block;
        margin-bottom: 8px;
        color: var(--soft);
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.18em;
        text-transform: uppercase;
      }}
      .field input {{
        width: 100%;
        padding: 13px 14px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.08);
        background: #07090d;
        color: var(--text);
        font: 12px var(--mono);
      }}
      .share-dialog .actions {{
        margin-top: 18px;
        display: flex;
        justify-content: flex-end;
        gap: 10px;
      }}
      .ghost-btn, .primary-btn {{
        border: none;
        padding: 12px 14px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        cursor: pointer;
      }}
      .ghost-btn {{
        background: rgba(255,255,255,0.05);
        color: var(--text);
      }}
      .primary-btn {{
        background: var(--white);
        color: #090a0e;
      }}
      .share-feedback {{
        margin-top: 14px;
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(62,213,152,0.12);
        color: #c8ffe7;
        display: none;
        font-size: 12px;
      }}
      .code-panel {{
        padding: 18px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        background: #05070a;
      }}
      pre {{
        margin: 0;
        white-space: pre-wrap;
        word-break: break-word;
        color: #dce4f5;
        font: 13px/1.55 var(--mono);
      }}
      .replay-layout {{
        display: grid;
        gap: 18px;
        grid-template-columns: 1.25fr 0.95fr;
      }}
      .terminal {{
        border-radius: 22px;
        border: 1px solid rgba(255,255,255,0.06);
        background: #06080c;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
        overflow: hidden;
      }}
      .terminal-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 16px 18px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
      }}
      .terminal-title {{
        color: #dfe6f3;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
      }}
      .lights {{
        display: flex;
        gap: 8px;
      }}
      .lights span {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #2a2f38;
      }}
      .replay-screen {{
        height: 420px;
        overflow: auto;
        padding: 18px;
        display: grid;
        gap: 12px;
      }}
      .event {{
        padding: 14px 16px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.02);
      }}
      .event-head {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
      }}
      .event-head strong {{
        font-size: 13px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }}
      .event-time {{
        color: var(--soft);
        font: 11px var(--mono);
      }}
      .event-detail {{
        margin-top: 8px;
        color: #c9d2e3;
        font-size: 13px;
        line-height: 1.55;
      }}
      .tone-info {{ border-color: rgba(126,176,255,0.12); }}
      .tone-stable {{ border-color: rgba(62,213,152,0.16); }}
      .tone-watch {{ border-color: rgba(244,190,85,0.16); }}
      .tone-review {{ border-color: rgba(255,93,115,0.18); background: rgba(255,93,115,0.05); }}
      .replay-controls {{
        display: grid;
        gap: 14px;
        margin-top: 16px;
        padding: 16px 18px 18px;
        border-top: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.02);
      }}
      .control-row {{
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
      }}
      .control-button {{
        border: 1px solid rgba(255,255,255,0.08);
        background: rgba(255,255,255,0.04);
        color: var(--text);
        padding: 10px 12px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        cursor: pointer;
      }}
      .control-button.primary {{
        background: var(--white);
        color: #0a0c12;
      }}
      .speed-btn.active {{
        background: rgba(79,124,255,0.18);
        border-color: rgba(79,124,255,0.28);
        color: var(--white);
      }}
      .seek {{
        width: 100%;
        accent-color: #f5f6fa;
      }}
      .seek-meta {{
        display: flex;
        justify-content: space-between;
        gap: 16px;
        color: var(--soft);
        font: 11px var(--mono);
      }}
      .stack {{
        display: grid;
        gap: 16px;
      }}
      .auth-tile {{
        padding: 16px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.06);
        background: rgba(255,255,255,0.025);
      }}
      .auth-tile .micro {{
        color: var(--soft);
        font-size: 10px;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-weight: 900;
      }}
      .auth-tile .value {{
        margin-top: 8px;
        font-size: 26px;
        font-weight: 900;
      }}
      .footer {{
        display: flex;
        flex-wrap: wrap;
        gap: 18px;
        margin-top: 18px;
        padding: 4px 6px 0;
        color: var(--soft);
        font-size: 11px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }}
      @keyframes pulse {{
        0%, 100% {{ box-shadow: 0 0 0 rgba(255,93,115,0); }}
        50% {{ box-shadow: 0 0 18px rgba(255,93,115,0.16); }}
      }}
      @media (max-width: 1160px) {{
        .shell {{ grid-template-columns: 1fr; }}
        .sidebar {{ display: none; }}
        .hero-grid, .stats-grid, .columns, .split, .share-grid, .replay-layout {{ grid-template-columns: 1fr; }}
      }}
    </style>
  </head>
  <body>
    <div class="shell">
      <aside class="sidebar">
        <div class="brand">
          <div class="brand-mark">∷</div>
          <strong>MCP // Recorder</strong>
          <span>Elegant Dark replay surface</span>
        </div>
        <div class="nav-label">Active views</div>
        {sidebar}
        <div class="side-meta">
          <div class="mini">
            <div class="micro">Total sessions</div>
            <div class="value">{summary["sessionCount"]}</div>
          </div>
          <div class="mini">
            <div class="micro">Review pressure</div>
            <div class="value">{summary["reviewSessions"]}</div>
          </div>
          <div class="mini">
            <div class="micro">Shared sessions</div>
            <div class="value">{summary["sharedSessions"]}</div>
          </div>
        </div>
      </aside>
      <main class="main">
        <div class="topbar">
          <div class="status-chip"><span class="status-dot"></span>Secure Uplink // Listening</div>
          <div class="topbar-right">
            <div class="operator-id">Operator ID<strong>mia.chen@kineticgain.com</strong></div>
            <a class="terminate" href="/docs">Terminate</a>
          </div>
        </div>
        <div class="wrap">
          <section class="hero">
            <div class="hero-grid">
              <div>
                <div class="eyebrow">MCP Session Recorder</div>
                <h1>{escape(title)}</h1>
                <div class="hero-subtitle">{escape(subtitle)}</div>
                <div class="hero-strip">{tabs}</div>
              </div>
              <div class="hero-side">
                <div class="panel-label">Elegant Dark control room</div>
                <div class="panel-title">Multi-operator replay, sharing, and evidence posture.</div>
                <div class="panel-copy">The recorder now surfaces owner-scoped sessions, explicit share grants, and richer playback controls so the screenshots actually tell the governance story.</div>
                <div class="glow-row">
                  <div class="glow-item"><span class="glow-dot"></span> Approval history attached</div>
                  <div class="glow-item"><span class="glow-dot"></span> Share matrix visible</div>
                  <div class="glow-item"><span class="glow-dot"></span> Session replay controls live</div>
                </div>
              </div>
            </div>
          </section>
          {body}
          <div class="footer">
            <span>Protocol: MCP-R-2026</span>
            <span>Theme: Elegant Dark</span>
            <span>Surface: approval-aware</span>
            <span>Mode: replay-ready</span>
          </div>
        </div>
      </main>
    </div>
    <div class="share-modal" id="share-modal">
      <div class="share-dialog">
        <h3>Share Session Chain</h3>
        <p>Invite another operator into the replay lane without exposing the full private session set. This is a product surface only here; the production-grade auth model is documented, not wired to Firebase in this FastAPI demo.</p>
        <div class="field">
          <label for="share-email">Operator Email</label>
          <input id="share-email" type="email" placeholder="operator@vault.mcp" />
        </div>
        <div class="actions">
          <button class="ghost-btn" id="share-cancel">Cancel</button>
          <button class="primary-btn" id="share-submit">Grant Access // Sync</button>
        </div>
        <div class="share-feedback" id="share-feedback">Access grant queued for review and evidence sync.</div>
      </div>
    </div>
    <script>
      (() => {{
        const modal = document.getElementById('share-modal');
        const feedback = document.getElementById('share-feedback');
        const emailInput = document.getElementById('share-email');
        const openers = document.querySelectorAll('[data-open-share]');
        const cancel = document.getElementById('share-cancel');
        const submit = document.getElementById('share-submit');
        openers.forEach((button) => button.addEventListener('click', () => {{
          modal.classList.add('open');
          feedback.style.display = 'none';
        }}));
        cancel?.addEventListener('click', () => modal.classList.remove('open'));
        modal?.addEventListener('click', (event) => {{
          if (event.target === modal) {{
            modal.classList.remove('open');
          }}
        }});
        submit?.addEventListener('click', () => {{
          const email = (emailInput.value || '').trim();
          if (!email) return;
          feedback.textContent = `Access grant staged for ${{email}}.`;
          feedback.style.display = 'block';
          emailInput.value = '';
        }});
      }})();
    </script>
    {page_script}
  </body>
</html>"""


def render_overview() -> str:
    summary = SERVICE.summary()
    auth = SERVICE.auth_posture()
    sessions = SERVICE.sessions_board()
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="label">Audit posture</div>
          <h2>Session reconstruction now looks like a real operator surface.</h2>
          <p>The best part of the AI Studio pass was not the chrome. It was the stronger story around authentication posture, sharing boundaries, and replay controls. Those ideas now show up in the actual app.</p>
        </div>
        <div class="section-body">
          <div class="stats-grid">
            <div class="stat"><div class="micro">Total sessions</div><div class="value">{summary["sessionCount"]}</div><div class="copy">Recorded MCP runs with replay, approvals, and evidence chains attached.</div></div>
            <div class="stat"><div class="micro">Review sessions</div><div class="value">{summary["reviewSessions"]}</div><div class="copy">Sessions that still carry destructive pressure or incomplete review evidence.</div></div>
            <div class="stat"><div class="micro">Shared sessions</div><div class="value">{summary["sharedSessions"]}</div><div class="copy">Owner-scoped runs that have been explicitly shared for audit or incident review.</div></div>
            <div class="stat"><div class="micro">Public sessions</div><div class="value">{summary["publicSessions"]}</div><div class="copy">Safe reference lanes that can be reused as baseline replay examples.</div></div>
          </div>
          <div class="columns" style="margin-top: 20px;">
            <div class="panel">
              <h3>Priority for replay</h3>
              <div class="mini-list">
                {_overview_mini(sessions)}
              </div>
            </div>
            <div class="panel">
              <h3>Authentication and sharing posture</h3>
              <div class="stack">
                <div class="auth-tile"><div class="micro">Owner-scoped sessions</div><div class="value">{auth["ownerScopedSessions"]}</div><div class="copy">{escape(auth["leadRecommendation"])}</div></div>
                <div class="auth-tile"><div class="micro">Private / shared / public</div><div class="value">{auth["privateSessions"]} / {auth["sharedSessions"]} / {auth["publicSessions"]}</div><div class="copy">The real product version could back this with Firebase Auth and strict document-level rules. The demo keeps the model visible without pretending the cloud layer exists here.</div></div>
              </div>
            </div>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div class="label">Top replay lanes</div>
          <h2>The highest-risk sessions stay in front of the operator.</h2>
          <p>Each lane shows the owner, share status, destructive path, and the action we would take next if this were a real review console.</p>
        </div>
        <div class="section-body">
          <div class="session-grid">
            {"".join(_session_card(session, include_share=True) for session in sessions)}
          </div>
        </div>
      </section>
    """
    return _shell(
        "Elegant replay control plane for MCP audit history.",
        "Authentication posture, share boundaries, and reconstructable session state for operator review.",
        "overview",
        body,
    )


def _overview_mini(sessions: list[dict]) -> str:
    items = []
    for session in sessions[:3]:
        items.append(
            f"""<div class="mini">
              <div class="micro">{escape(session["serverName"])}</div>
              <div class="title">{escape(session["nextAction"])}</div>
              <div class="desc">{escape(session["operator"])} · {escape(session["visibility"])} visibility · {len(session["sharedWith"])} collaborators</div>
            </div>"""
        )
    return "".join(items)


def _session_card(session: dict, include_share: bool = False) -> str:
    tools = "".join(f'<span class="pill">{escape(tool["name"])}</span>' for tool in session["toolCalls"])
    trail = "".join(
        f'<div class="mini"><div class="micro">Evidence note</div><div class="desc">{escape(note)}</div></div>'
        for note in session["evidenceTrail"][:2]
    )
    share_copy = (
        f'<div class="meta">Owner: {escape(session["ownerEmail"])} · Visibility: {escape(session["visibility"])} · Shared with {len(session["sharedWith"])} operator(s)</div>'
        if include_share
        else ""
    )
    return f"""
      <div class="session-card">
        <div class="session-top">
          <div>
            <h3>{escape(session["serverName"])}</h3>
            <div class="meta">{escape(session["sessionId"])} · {escape(session["operator"])} · {escape(session["environment"])} · {escape(session["authModel"])}</div>
            {share_copy}
          </div>
          <span class="tag {_status_class(session["verdict"])}">{escape(session["verdict"])}</span>
          <div class="score-stack"><div class="micro">Risk score</div><div class="value">{session["riskScore"]}</div></div>
        </div>
        <div class="session-bottom">
          <div class="split">
            <div>
              <div class="mini"><div class="micro">Next action</div><div class="title">{escape(session["nextAction"])}</div><div class="desc">Approval: {escape(session["humanApproval"])} · Evidence {session["evidenceCoverage"]}% · Citations {session["citationCoverage"]}%</div></div>
              <div class="pill-row">{tools}</div>
            </div>
            <div class="mini-list">{trail}</div>
          </div>
        </div>
      </div>
    """


def render_sessions() -> str:
    rows = "".join(
        f"""
        <tr>
          <td><strong>{escape(session["sessionId"])}</strong><div class="subtext">{escape(session["serverName"])} · {escape(session["operator"])}</div></td>
          <td>{escape(session["ownerEmail"])}</td>
          <td>{escape(session["visibility"])}</td>
          <td>{len(session["sharedWith"])}</td>
          <td>{session["evidenceCoverage"]}%</td>
          <td>{session["citationCoverage"]}%</td>
        </tr>
        """
        for session in SERVICE.sessions_board()
    )
    share_cards = "".join(
        f"""
        <div class="share-card">
          <div class="header">
            <div>
              <div class="micro">{escape(item["sessionId"])}</div>
              <strong>{escape(item["serverName"])}</strong>
            </div>
            <span class="tag {'stable' if item['visibility'] == 'public' else 'watch' if item['visibility'] == 'shared' else 'review'}">{escape(item["visibility"])}</span>
          </div>
          <div class="meta">Owner: {escape(item["ownerEmail"])}</div>
          <div class="share-list">
            {"".join(f"<div>{escape(email)}</div>" for email in item["sharedWith"]) if item["sharedWith"] else "<div>No collaborators granted</div>"}
          </div>
          <div style="margin-top: 14px;">
            <button class="share-button" data-open-share>Share Session Chain</button>
          </div>
        </div>
        """
        for item in SERVICE.share_matrix()
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="label">Session inventory</div>
          <h2>Session isolation, ownership, and share grants are now explicit.</h2>
          <p>The inventory surface now makes it obvious which sessions are owner-only, which are shareable, and which are safe enough to act as public replay references.</p>
        </div>
        <div class="section-body">
          <div class="table-shell">
            <table>
              <thead>
                <tr>
                  <th>Session identity</th>
                  <th>Owner</th>
                  <th>Visibility</th>
                  <th>Shared with</th>
                  <th>Evidence</th>
                  <th>Citations</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="section-head">
          <div class="label">Share matrix</div>
          <h2>Collaborative review without flattening the privacy model.</h2>
          <p>This takes the best idea from the AI Studio version and keeps it honest: explicit owner and shared-with lanes, without pretending this demo is running a production Firebase stack.</p>
        </div>
        <div class="section-body">
          <div class="share-grid">{share_cards}</div>
        </div>
      </section>
    """
    return _shell(
        "Session inventory for owner scope and sharing posture.",
        "Owner emails, visibility lanes, and explicit collaborator grants for every recorded MCP run.",
        "sessions",
        body,
    )


def render_approvals() -> str:
    approvals = SERVICE.approval_board()
    share = SERVICE.share_matrix()
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
        for row in approvals
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="label">Approval history</div>
          <h2>The command chain stays attached to the run.</h2>
          <p>Approvals look stronger when you can see them in the same product surface as share boundaries and evidence depth instead of in three separate systems.</p>
        </div>
        <div class="section-body">
          <div class="columns">
            <div class="table-shell">
              <table>
                <thead>
                  <tr>
                    <th>Review step</th>
                    <th>Owner</th>
                    <th>Status</th>
                    <th>Timestamp</th>
                    <th>Risk</th>
                  </tr>
                </thead>
                <tbody>{rows}</tbody>
              </table>
            </div>
            <div class="panel">
              <h3>Share-aware review notes</h3>
              <div class="mini-list">
                {"".join(
                    f'<div class="mini"><div class="micro">{escape(item["serverName"])}</div><div class="title">{escape(item["visibility"])} visibility · {item["sharedCount"]} collaborators</div><div class="desc">Owner lane: {escape(item["ownerEmail"])}</div></div>'
                    for item in share[:3]
                )}
              </div>
            </div>
          </div>
        </div>
      </section>
    """
    return _shell(
        "Approval history with ownership and sharing context.",
        "Human signoff remains visible alongside ownership and evidence posture.",
        "approvals",
        body,
    )


def render_replay() -> str:
    sessions = SERVICE.sessions_board()
    payload = json.dumps(sessions, indent=2)
    event_data = json.dumps(
        {
            "sessions": [
                {
                    "sessionId": session["sessionId"],
                    "serverName": session["serverName"],
                    "operator": session["operator"],
                    "visibility": session["visibility"],
                    "sharedWith": session["sharedWith"],
                    "riskScore": session["riskScore"],
                    "verdict": session["verdict"],
                    "events": session["replayEvents"],
                }
                for session in sessions
            ]
        }
    )
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="label">Session replay</div>
          <h2>Playback controls, temporal seeking, and share-aware reconstruction.</h2>
          <p>The replay view now borrows the best product idea from the AI Studio build: a real control surface for stepping through the session instead of a static block of explanatory text.</p>
        </div>
        <div class="section-body">
          <div class="replay-layout">
            <div class="terminal">
              <div class="terminal-head">
                <div class="terminal-title" id="replay-title">Growth Ops MCP // Replay</div>
                <div class="lights"><span></span><span></span><span></span></div>
              </div>
              <div class="replay-screen" id="replay-screen"></div>
              <div class="replay-controls">
                <div class="control-row">
                  <button class="control-button primary" id="play-toggle">Play</button>
                  <button class="control-button" data-open-share>Share Session Chain</button>
                  <select class="control-button" id="session-select">
                    {"".join(f'<option value="{escape(session["sessionId"])}">{escape(session["serverName"])} · {escape(session["sessionId"])}</option>' for session in sessions)}
                  </select>
                </div>
                <input class="seek" id="seek" type="range" min="0" max="4" value="0" />
                <div class="seek-meta">
                  <span id="seek-left">00:00 // Session start</span>
                  <span id="seek-right">Ready for reconstruction</span>
                </div>
                <div class="control-row">
                  <button class="control-button speed-btn active" data-speed="1">1x</button>
                  <button class="control-button speed-btn" data-speed="2">2x</button>
                  <button class="control-button speed-btn" data-speed="4">4x</button>
                </div>
              </div>
            </div>
            <div class="stack">
              <div class="panel">
                <h3>Replay posture</h3>
                <div class="mini-list">
                  <div class="mini"><div class="micro">What improved</div><div class="title">Temporal controls are now visible.</div><div class="desc">Play, pause, seek, and speed controls make the replay surface look like an audit tool instead of a placeholder.</div></div>
                  <div class="mini"><div class="micro">What stayed honest</div><div class="title">No fake Firebase claim in the code.</div><div class="desc">The docs explain how owner and shared-with fields would map to a hardened backend, but the demo stays local-first and truthful.</div></div>
                  <div class="mini"><div class="micro">Current focus</div><div class="title">Destructive paths first.</div><div class="desc">The default replay lane opens on the highest-risk session so the screenshots immediately show the real problem surface.</div></div>
                </div>
              </div>
              <div class="code-panel">
                <pre>{escape(payload)}</pre>
              </div>
            </div>
          </div>
        </div>
      </section>
    """
    script = f"""
    <script>
      (() => {{
        const data = {event_data};
        const screen = document.getElementById('replay-screen');
        const title = document.getElementById('replay-title');
        const playToggle = document.getElementById('play-toggle');
        const seek = document.getElementById('seek');
        const seekLeft = document.getElementById('seek-left');
        const seekRight = document.getElementById('seek-right');
        const speedButtons = Array.from(document.querySelectorAll('.speed-btn'));
        const sessionSelect = document.getElementById('session-select');
        let currentSession = data.sessions[0];
        let currentIndex = 0;
        let playing = false;
        let speed = 1;
        let timer = null;

        function timeLabel(seconds) {{
          const mins = String(Math.floor(seconds / 60)).padStart(2, '0');
          const secs = String(seconds % 60).padStart(2, '0');
          return `${{mins}}:${{secs}}`;
        }}

        function render() {{
          title.textContent = `${{currentSession.serverName}} // Replay`;
          const events = currentSession.events.slice(0, currentIndex + 1);
          if (!events.length) {{
            screen.innerHTML = '<div class="mini"><div class="micro">Replay state</div><div class="desc">Ready for reconstruction. Press play to begin stepping through the session.</div></div>';
            seekLeft.textContent = '00:00 // Session start';
            seekRight.textContent = 'Ready for reconstruction';
            return;
          }}
          screen.innerHTML = events.map((event) => `
            <div class="event ${{event.severity === 'review' ? 'tone-review' : event.severity === 'watch' ? 'tone-watch' : event.severity === 'stable' ? 'tone-stable' : 'tone-info'}}">
              <div class="event-head">
                <strong>${{event.label}}</strong>
                <span class="event-time">${{timeLabel(event.offsetSeconds)}}</span>
              </div>
              <div class="event-detail">${{event.detail}}</div>
            </div>
          `).join('');
          const active = events[events.length - 1];
          seekLeft.textContent = `${{timeLabel(active.offsetSeconds)}} // ${{
            currentSession.visibility
          }} visibility`;
          seekRight.textContent = `${{currentSession.sharedWith.length}} share grants // risk ${{
            currentSession.riskScore
          }}`;
          screen.scrollTop = screen.scrollHeight;
        }}

        function syncSeek() {{
          seek.max = Math.max(currentSession.events.length - 1, 0);
          seek.value = currentIndex;
        }}

        function stopTimer() {{
          if (timer) {{
            clearInterval(timer);
            timer = null;
          }}
        }}

        function startTimer() {{
          stopTimer();
          timer = setInterval(() => {{
            if (currentIndex >= currentSession.events.length - 1) {{
              playing = false;
              playToggle.textContent = 'Play';
              stopTimer();
              return;
            }}
            currentIndex += 1;
            syncSeek();
            render();
          }}, 1800 / speed);
        }}

        playToggle.addEventListener('click', () => {{
          playing = !playing;
          playToggle.textContent = playing ? 'Pause' : 'Play';
          if (playing) {{
            startTimer();
          }} else {{
            stopTimer();
          }}
        }});

        seek.addEventListener('input', (event) => {{
          currentIndex = Number(event.target.value);
          render();
        }});

        sessionSelect.addEventListener('change', (event) => {{
          currentSession = data.sessions.find((item) => item.sessionId === event.target.value) || data.sessions[0];
          currentIndex = 0;
          playing = false;
          playToggle.textContent = 'Play';
          stopTimer();
          syncSeek();
          render();
        }});

        speedButtons.forEach((button) => {{
          button.addEventListener('click', () => {{
            speed = Number(button.dataset.speed);
            speedButtons.forEach((item) => item.classList.remove('active'));
            button.classList.add('active');
            if (playing) {{
              startTimer();
            }}
          }});
        }});

        syncSeek();
        render();
      }})();
    </script>
    """
    return _shell(
        "Elegant dark replay console for MCP session reconstruction.",
        "Playback controls, share-aware session state, and real-time event filtering for audit review.",
        "replay",
        body,
        script,
    )


def render_docs() -> str:
    payload = json.dumps(SERVICE.auth_posture(), indent=2)
    body = f"""
      <section class="section">
        <div class="section-head">
          <div class="label">Architecture</div>
          <h2>What we borrowed from AI Studio and what we deliberately did not.</h2>
          <p>The best ideas were product-shape ideas: owner-scoped sessions, explicit share grants, better replay controls, and a cleaner elegant-dark hierarchy. The repo now reflects those strengths without faking a cloud backend we did not actually wire.</p>
        </div>
        <div class="section-body">
          <div class="columns">
            <div class="panel">
              <h3>Implemented in the real repo</h3>
              <div class="mini-list">
                <div class="mini"><div class="micro">Replay controls</div><div class="title">Play, pause, seek, and speed lanes.</div><div class="desc">The `/replay` surface now behaves like a reconstruction console instead of a static explanation page.</div></div>
                <div class="mini"><div class="micro">Ownership model</div><div class="title">Owner email, visibility, and shared-with lanes.</div><div class="desc">Session data now carries the collaboration model directly so the proof surfaces can explain who should see what.</div></div>
                <div class="mini"><div class="micro">Better proof assets</div><div class="title">Real page captures replace underpowered screenshots.</div><div class="desc">The screenshot generator now captures actual live routes instead of relying on thin visual summaries.</div></div>
              </div>
            </div>
            <div class="panel">
              <h3>Documented, not faked</h3>
              <div class="mini-list">
                <div class="mini"><div class="micro">Authentication</div><div class="title">Firebase-style auth is described as a production direction.</div><div class="desc">The repo now explains how secure uplink and owner/session isolation would map to a real backend without pretending the local FastAPI demo already does it.</div></div>
                <div class="mini"><div class="micro">Security rules</div><div class="title">Share grants would pair with document-level access controls.</div><div class="desc">That is the right story for a future production build, but not something we should counterfeit inside a static sample repo.</div></div>
              </div>
              <div class="code-panel" style="margin-top: 16px;">
                <pre>{escape(payload)}</pre>
              </div>
            </div>
          </div>
        </div>
      </section>
    """
    return _shell(
        "Architecture and product-shape notes.",
        "A cleaner explanation of what is implemented now versus what belongs to a future cloud-backed production version.",
        "docs",
        body,
    )
