from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

pattern = re.compile(r"from\s+scripts\.lib\.([A-Za-z0-9_]+)\s+import")

print("=" * 50)
print("LENABA IMPORT DOCTOR")
print("=" * 50)

count = 0

for file in SCRIPTS.rglob("*.py"):

    text = file.read_text(encoding="utf-8")

    for m in pattern.finditer(text):

        count += 1

        print(file.relative_to(ROOT))
        print(f"  scripts.lib.{m.group(1)}")
        print()

print(f"Remaining legacy imports: {count}")
