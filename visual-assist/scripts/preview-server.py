#!/usr/bin/env python3
"""Deterministic local preview server for visual-assist pages.

Usage:
  preview-server.py <workspace> [--foreground]
  preview-server.py --serve <visuals-root> <port> [--foreground]

The port is derived deterministically from the absolute workspace path
(DJB2 hash mod 301 + 38700), matching the visual-assist convention across
harnesses. A running server is detected through a health endpoint that
reports the exact directory it serves, so a second invocation reuses it
instead of guessing. The server binds 127.0.0.1 only.

Exit codes:
  0  success (prints the preview origin and reuse status)
  2  the workspace port is occupied by a foreign service
  3  no python http server could be started or verified
  4  .agents/visuals missing under the workspace
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

HEALTH_PATH = "/__visual_assist_health"
PORT_BASE = 38700
PORT_SPAN = 301


def djb2(value: str) -> int:
    """DJB2 over code points with 32-bit wrapping, matching the JS reference."""
    h = 5381
    for ch in value:
        h = (((h * 33) & 0xFFFFFFFF) ^ ord(ch)) & 0xFFFFFFFF
    return h


def port_for(workspace: str) -> int:
    return PORT_BASE + djb2(workspace) % PORT_SPAN


class VisualsHandler(SimpleHTTPRequestHandler):
    """Static handler with an identity health endpoint and no listings."""

    root: str = ""

    def do_GET(self):  # noqa: N802 - stdlib naming
        if self.path == HEALTH_PATH:
            body = json.dumps({"root": self.root}).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()

    def list_directory(self, path):  # noqa: ARG002 - disable listings
        self.send_error(404, "Not found")
        return None

    def log_message(self, fmt: str, *args: object) -> None:  # keep logs quiet
        pass


def serve_forever(root: str, port: int) -> None:
    VisualsHandler.root = root
    os.chdir(root)
    server = HTTPServer(("127.0.0.1", port), VisualsHandler)
    server.serve_forever()


def health_matches(port: int, root: str) -> bool:
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{port}{HEALTH_PATH}", timeout=1.5
        ) as response:
            if response.status != 200:
                return False
            return json.loads(response.read().decode()).get("root") == root
    except (OSError, ValueError):
        return False


def port_is_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
        probe.settimeout(0.5)
        return probe.connect_ex(("127.0.0.1", port)) != 0


def verify_page(url: str) -> None:
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            if response.status != 200:
                raise RuntimeError(f"preview returned HTTP {response.status}")
            ctype = response.headers.get("Content-Type", "")
            if "text/html" not in ctype:
                raise RuntimeError("preview did not return HTML")
    except (OSError, RuntimeError) as error:
        raise RuntimeError(f"preview verification failed: {error}") from error


def main(argv: list[str]) -> int:
    foreground = "--foreground" in argv
    argv = [a for a in argv if a != "--foreground"]

    if argv and argv[0] == "--serve":
        if len(argv) != 3:
            print("usage: preview-server.py --serve <visuals-root> <port>", file=sys.stderr)
            return 3
        serve_forever(argv[1], int(argv[2]))
        return 0

    workspace = Path(argv[0] if argv else os.getcwd()).resolve()
    root = workspace / ".agents" / "visuals"
    if not root.is_dir():
        print(f"missing directory: {root}", file=sys.stderr)
        return 4
    root = str(root.resolve())
    port = port_for(str(workspace))

    if health_matches(port, root):
        print(f"status=reused")
        print(f"origin=http://localhost:{port}")
        return 0

    if not port_is_free(port):
        print(
            f"port {port} is occupied by a foreign service; do not use another port or server",
            file=sys.stderr,
        )
        return 2

    if foreground:
        serve_forever(root, port)
        return 0

    log = Path(tempfile.gettempdir()) / f"visual-assist-{port}.log"
    with open(log, "wb") as sink:
        subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), "--serve", root, str(port)],
            stdout=sink,
            stderr=sink,
            start_new_session=True,
        )
    for _ in range(50):
        if health_matches(port, root):
            print("status=started")
            print(f"origin=http://localhost:{port}")
            return 0
        time.sleep(0.1)
    print("server did not become healthy", file=sys.stderr)
    return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
