"""Exercise the real local server and a restart using an isolated temporary dataset."""

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def server(database, port, log, memory=False):
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
    with log.open("a") as output:
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "solid_workbook.backend",
                *(["--memory"] if memory else ["--database", str(database)]),
                "--port",
                str(port),
            ],
            env=env,
            stdout=output,
            stderr=subprocess.STDOUT,
            cwd=ROOT,
        )
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    raise RuntimeError(log.read_text())
                try:
                    with urlopen(
                        f"http://127.0.0.1:{port}/ready", timeout=0.3
                    ) as response:
                        if response.status == 200:
                            break
                except (URLError, TimeoutError):
                    time.sleep(0.05)
            else:
                raise RuntimeError("Server readiness timed out")
            yield
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def main():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        port = listener.getsockname()[1]
    base = f"http://127.0.0.1:{port}"
    payload = {"identity": "smoke-001", "station": "North ridge", "kelvin": 281.25}

    def request(path, method="GET", body=None):
        data = None if body is None else json.dumps(body).encode()
        headers = {"Content-Type": "application/json", "Idempotency-Key": "smoke-001"}
        with urlopen(
            Request(base + path, data=data, method=method, headers=headers), timeout=3
        ) as response:
            return response.status, json.load(response)

    with tempfile.TemporaryDirectory() as directory:
        database = Path(directory) / "notebook.sqlite3"
        log = Path(directory) / "server.log"
        with server(database, port, log):
            assert request("/readings", "POST", payload)[0] == 201
            assert request("/readings", "POST", payload)[0] == 200
            assert len(request("/export?format=json")[1]) == 1
        with server(database, port, log):
            assert request("/readings/smoke-001")[1]["observation"] == payload
            assert request("/readings", "POST", payload)[0] == 200
            assert request("/outbox/process", "POST")[1]["outcome"] == "acknowledged"
            assert request("/outbox/process", "POST")[1]["outcome"] == "empty"
        with server(database, port, log, memory=True):
            assert request("/readings")[1]["readings"] == []
            assert request("/readings", "POST", payload)[0] == 201
        with server(database, port, log, memory=True):
            assert request("/readings")[1]["readings"] == []
    print("Live HTTP, persistent SQLite restart and ephemeral memory checks passed.")


if __name__ == "__main__":
    main()
