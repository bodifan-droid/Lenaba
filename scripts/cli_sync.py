
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

CLI = ROOT / "scripts" / "cli.py"
BUILDERS = ROOT / "scripts" / "builders"
AUDITS = ROOT / "scripts" / "audits"


def extract_commands(text: str):

    pattern = re.compile(r'\("([^"]+)",\s*"([^"]+)"\)')

    return {
        (group, name)
        for group, name in pattern.findall(text)
    }


def main():

    cli_text = CLI.read_text(encoding="utf-8")

    mapped = extract_commands(cli_text)

    builder_files = {
        ("build", p.stem.replace("build_", ""))
        for p in BUILDERS.glob("*.py")
    }

    audit_files = {
        ("audit", p.stem.replace("audit_", ""))
        for p in AUDITS.glob("*.py")
    }

    discovered = builder_files | audit_files

    missing = sorted(discovered - mapped)
    orphan = sorted(mapped - discovered)

    print("=" * 50)
    print("LENABA CLI SYNC")
    print("=" * 50)

    print(f"Builders found : {len(builder_files)}")
    print(f"Audits found   : {len(audit_files)}")
    print(f"Mapped commands: {len(mapped)}")

    print()

    if missing:
        print("Missing CLI commands:")
        for group, name in missing:
            print(f"  + {group} {name}")
    else:
        print("No missing commands.")

    print()

    if orphan:
        print("Orphan CLI commands:")
        for group, name in orphan:
            print(f"  - {group} {name}")
    else:
        print("No orphan commands.")

    print()

    if not missing and not orphan:
        print("✓ CLI synchronized")


if __name__ == "__main__":
    main()
