from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "screenshots"
OUT_DIR.mkdir(exist_ok=True)


def edge_path() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Microsoft Edge not found")


def main() -> None:
    for item in OUT_DIR.iterdir():
        if item.is_file():
            item.unlink()

    python_exe = ROOT / ".venv" / "Scripts" / "python.exe"
    if not python_exe.exists():
        raise FileNotFoundError("Virtual environment not found")

    server = subprocess.Popen(
        [str(python_exe), "-m", "app.main"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        time.sleep(3)
        browser = edge_path()
        shots = [
            ("01-overview.png", "http://127.0.0.1:5018/"),
            ("02-sessions.png", "http://127.0.0.1:5018/sessions"),
            ("03-approvals.png", "http://127.0.0.1:5018/approvals"),
            ("04-replay.png", "http://127.0.0.1:5018/replay"),
        ]
        for filename, url in shots:
            target = OUT_DIR / filename
            command = [
                str(browser),
                "--headless",
                "--disable-gpu",
                "--hide-scrollbars",
                "--window-size=1600,1000",
                "--virtual-time-budget=6000",
                f"--screenshot={target}",
                url,
            ]
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()
            server.wait(timeout=5)

    print("rendered")


if __name__ == "__main__":
    main()
