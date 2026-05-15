from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_session_data.json"


@dataclass
class SessionRecorderService:
    catalog: dict
    sessions: list[dict]

    def summary(self) -> dict:
        review_sessions = sum(1 for session in self.sessions if session["verdict"] == "review")
        watch_sessions = sum(1 for session in self.sessions if session["verdict"] == "watch")
        stable_sessions = sum(1 for session in self.sessions if session["verdict"] == "stable")
        approval_required = sum(1 for session in self.sessions if session["humanApproval"] == "required")
        destructive_calls = sum(
            1
            for session in self.sessions
            for tool in session["toolCalls"]
            if tool["destructive"]
        )
        return {
            "sessionCount": len(self.sessions),
            "reviewSessions": review_sessions,
            "watchSessions": watch_sessions,
            "stableSessions": stable_sessions,
            "approvalRequiredSessions": approval_required,
            "destructiveToolCalls": destructive_calls,
            "averageRiskScore": round(mean(session["riskScore"] for session in self.sessions), 1),
            "averageEvidenceCoverage": round(mean(session["evidenceCoverage"] for session in self.sessions), 1),
            "averageCitationCoverage": round(mean(session["citationCoverage"] for session in self.sessions), 1),
            "leadRecommendation": self._lead_recommendation(),
        }

    def sessions_board(self) -> list[dict]:
        verdict_weight = {"review": 3, "watch": 2, "stable": 1}
        return sorted(
            self.sessions,
            key=lambda session: (
                verdict_weight[session["verdict"]],
                session["riskScore"],
                session["startedAt"],
            ),
            reverse=True,
        )

    def session_detail(self, session_id: str) -> dict | None:
        return next((session for session in self.sessions if session["sessionId"] == session_id), None)

    def approval_board(self) -> list[dict]:
        rows: list[dict] = []
        for session in self.sessions_board():
            for approval in session["approvals"]:
                rows.append(
                    {
                        "sessionId": session["sessionId"],
                        "serverName": session["serverName"],
                        "operator": session["operator"],
                        "riskScore": session["riskScore"],
                        "step": approval["step"],
                        "owner": approval["owner"],
                        "status": approval["status"],
                        "timestamp": approval["timestamp"],
                    }
                )
        status_weight = {"open": 2, "completed": 1}
        return sorted(rows, key=lambda row: (status_weight[row["status"]], row["timestamp"]), reverse=True)

    def replay_board(self) -> list[dict]:
        rows = []
        for session in self.sessions_board():
            artifact_count = sum(tool["evidenceArtifacts"] for tool in session["toolCalls"])
            missing_citations = sum(1 for tool in session["toolCalls"] if tool["citations"] == 0)
            rows.append(
                {
                    "sessionId": session["sessionId"],
                    "serverName": session["serverName"],
                    "operator": session["operator"],
                    "verdict": session["verdict"],
                    "riskScore": session["riskScore"],
                    "artifactCount": artifact_count,
                    "missingCitations": missing_citations,
                    "nextAction": session["nextAction"],
                }
            )
        return rows

    def sample_payload(self) -> dict:
        sessions = self.sessions_board()
        return {
            "dashboard": self.summary(),
            "prioritySession": {
                "sessionId": sessions[0]["sessionId"],
                "serverName": sessions[0]["serverName"],
                "riskScore": sessions[0]["riskScore"],
                "verdict": sessions[0]["verdict"],
                "nextAction": sessions[0]["nextAction"],
            },
            "openApprovals": [row for row in self.approval_board() if row["status"] == "open"],
        }

    def recollection(self, prompt: str) -> dict:
        tokens = {token.strip(".,:;!?").lower() for token in prompt.split() if token.strip()}
        ranked = []
        for session in self.sessions:
            score = 0
            searchable = " ".join(
                [
                    session["serverName"],
                    session["serverOwner"],
                    session["operator"],
                    session["nextAction"],
                    " ".join(tool["name"] for tool in session["toolCalls"]),
                ]
            ).lower()
            for token in tokens:
                if token in searchable:
                    score += 8
            if session["verdict"] == "review":
                score += 18
            elif session["verdict"] == "watch":
                score += 10
            score += int(session["riskScore"] / 6)
            score += max(0, 10 - session["approvalLatencyMinutes"])
            score += max(0, session["evidenceCoverage"] // 20)
            ranked.append(
                {
                    "sessionId": session["sessionId"],
                    "serverName": session["serverName"],
                    "operator": session["operator"],
                    "verdict": session["verdict"],
                    "riskScore": session["riskScore"],
                    "score": score,
                    "nextAction": session["nextAction"],
                }
            )
        ranked.sort(key=lambda item: item["score"], reverse=True)
        return {
            "prompt": prompt,
            "topSession": ranked[0],
            "nextAction": ranked[0]["nextAction"],
            "rankedSessions": ranked[:3],
        }

    def _lead_recommendation(self) -> str:
        high_risk = [session for session in self.sessions if session["verdict"] == "review"]
        if high_risk:
            return "Hold any destructive MCP lane behind replayable approval evidence until the open review sessions clear."
        watch = [session for session in self.sessions if session["verdict"] == "watch"]
        if watch:
            return "Use the recorder to deepen citation and evidence chains before those watch lanes become formal review pressure."
        return "Current session evidence is stable enough to expand trusted operator workflows cautiously."


def build_service() -> SessionRecorderService:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return SessionRecorderService(catalog=payload["catalog"], sessions=payload["sessions"])
