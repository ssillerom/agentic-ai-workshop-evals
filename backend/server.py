from __future__ import annotations

import argparse

import uvicorn

from .settings import get_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Dad IT Support Agent Python server.")
    parser.add_argument("--reload", action="store_true", help="Reload when Python files change.")
    args = parser.parse_args()

    settings = get_settings()
    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=settings.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()
