from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app


def main() -> None:
    client = TestClient(app)
    checks = [
        ("/", "GET"),
        ("/sessions", "GET"),
        ("/approvals", "GET"),
        ("/replay", "GET"),
        ("/docs", "GET"),
        ("/api/dashboard/summary", "GET"),
        ("/api/sessions", "GET"),
        ("/api/approvals", "GET"),
        ("/api/replay", "GET"),
        ("/api/shares", "GET"),
        ("/api/auth-posture", "GET"),
        ("/api/sample", "GET"),
    ]
    for path, method in checks:
      response = client.request(method, path)
      assert response.status_code == 200, f"{path} returned {response.status_code}"

    response = client.post(
        "/api/recollect",
        json={"prompt": "Need replay context for destructive approval gaps in the growth ops server."},
    )
    assert response.status_code == 200, "/api/recollect failed"
    print("smoke-ok")


if __name__ == "__main__":
    main()
