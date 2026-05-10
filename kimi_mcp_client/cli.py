"""Backward-compatible CLI shim to new `kimi_mcp_client.main` entrypoint."""

from .main import main


if __name__ == "__main__":
    raise SystemExit(main())
