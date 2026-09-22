
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.behind_parser import parse_name_page
from lib.master_writer import write_to_master

CACHE = ROOT / "data" / "cache" / "behind_html"


def display_name(path: Path):
    return path.stem.replace("-", " ").title()


def main():

    files = sorted(CACHE.glob("*.html"))

    print("=" * 50)
    print("RETRO IMPORT FROM HTML CACHE")
    print("=" * 50)
    print(f"Cached pages: {len(files)}")

    updated_pages = 0
    updated_fields = 0

    for html_file in files:

        html = html_file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        parsed = parse_name_page(html)

        if not parsed:
            continue

        name = parsed.get("canonical_name") or display_name(html_file)

        updated = write_to_master(name, parsed)

        if updated:
            updated_pages += 1
            updated_fields += updated

    print("-" * 50)
    print(f"Pages updated : {updated_pages}")
    print(f"Fields written: {updated_fields}")
    print("=" * 50)


if __name__ == "__main__":
    main()
