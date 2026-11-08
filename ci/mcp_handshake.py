#!/usr/bin/env python3
"""CI smoke test: MCP handshake against the packaged server.

Starts server/src/server.py with the venv interpreter (no DaVinci Resolve on
CI — the server must still answer protocol messages), speaks newline-delimited
JSON-RPC, and asserts the initialize handshake and a non-trivial tools/list.
"""
import json
import subprocess
import sys

CMD = ["./server/venv/bin/python", "./server/src/server.py"]
MIN_TOOLS = 30


def main():
    proc = subprocess.Popen(
        CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    try:
        def send(msg):
            proc.stdin.write(json.dumps(msg) + "\n")
            proc.stdin.flush()

        def read_response(req_id):
            while True:
                line = proc.stdout.readline()
                if not line:
                    raise RuntimeError("server closed stdout without answering")
                msg = json.loads(line)
                if msg.get("id") == req_id:
                    return msg

        send({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ci-smoke", "version": "1"},
            },
        })
        init = read_response(1)
        server_info = init.get("result", {}).get("serverInfo", {})
        if server_info.get("name") != "DaVinciResolveMCP":
            raise RuntimeError(f"unexpected serverInfo: {server_info}")
        print(f"initialize OK: {server_info.get('name')} v{server_info.get('version')}")

        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = read_response(2).get("result", {}).get("tools", [])
        print(f"tools/list OK: {len(tools)} tools")
        if len(tools) < MIN_TOOLS:
            raise RuntimeError(f"expected at least {MIN_TOOLS} tools, got {len(tools)}")

        print("MCP smoke test passed")
    finally:
        proc.kill()
        proc.wait()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
