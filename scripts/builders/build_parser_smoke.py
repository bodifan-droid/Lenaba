
from __future__ import annotations

from pathlib import Path
from pprint import pprint

from scripts.lib.behind_parser import parse_name_page

HTML = Path("tests/html/yamila.html")


def main():

    html = HTML.read_text(encoding="utf-8")

    result = parse_name_page(html)

    print("=" * 45)
    print("BEHIND PARSER TEST")
    print("=" * 45)

    pprint(result)


if __name__ == "__main__":
    main()
