from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


COMMANDS = {
    "fetch": ROOT / "executors" / "fetch_doctor.py",
    "prompt": ROOT / "executors" / "prompt_doctor.py",
    "queue": ROOT / "executors" / "queue_orchestrator.py",
}


def run_script(script: Path, args: list[str]):

    if not script.exists():
        print(f"Missing: {script}")
        return

    subprocess.run(
        [sys.executable, str(script), *args],
        check=False,
    )


def health():

    print("=" * 40)
    print("LENABA HEALTH")
    print("=" * 40)
    print()

    checks = {
        "execution_queue": ROOT.parent / "data" / "knowledge" / "execution_queue.parquet",
        "family_scripts": ROOT.parent / "data" / "knowledge" / "family_scripts.parquet",
        "names": ROOT.parent / "data" / "enriched" / "names.parquet",
        "knowledge_cache": ROOT.parent / "data" / "cache" / "knowledge_cache.parquet",
    }

    for name, path in checks.items():

        status = "✓" if path.exists() else "✗"

        print(f"{status} {name}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "command",
        choices=["fetch", "prompt", "queue", "health"],
    )

    parser.add_argument("name", nargs="?")

    args = parser.parse_args()

    if args.command == "health":
        health()
        return

    run_script(COMMANDS[args.command], [args.name] if args.name else [])


if __name__ == "__main__":
    main()
