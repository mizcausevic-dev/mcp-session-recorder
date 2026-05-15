from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.session_service import build_service


def main() -> None:
    service = build_service()
    payload = {
        "dashboard": service.summary(),
        "prioritySession": service.sessions_board()[0],
        "recollection": service.recollection(
            "Need replay context for destructive approval gaps in the growth ops server."
        ),
    }
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
