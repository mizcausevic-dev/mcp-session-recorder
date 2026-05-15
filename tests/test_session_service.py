from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from app.main import app
from app.services.session_service import build_service


class MCPSessionRecorderTests(unittest.TestCase):
    def test_summary_shape(self) -> None:
        summary = build_service().summary()
        self.assertEqual(summary["sessionCount"], 4)
        self.assertGreaterEqual(summary["destructiveToolCalls"], 4)
        self.assertIn("leadRecommendation", summary)

    def test_recollection_returns_ranked_results(self) -> None:
        payload = build_service().recollection("Need destructive approval replay context")
        self.assertEqual(len(payload["rankedSessions"]), 3)
        self.assertIn("topSession", payload)

    def test_session_lookup_api(self) -> None:
        client = TestClient(app)
        response = client.get("/api/sessions/mcp-sess-1042")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["serverName"], "Growth Ops MCP")

    def test_share_matrix_api(self) -> None:
        client = TestClient(app)
        response = client.get("/api/shares")
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(payload[0]["sharedCount"], 0)
        self.assertIn("visibility", payload[0])


if __name__ == "__main__":
    unittest.main()
