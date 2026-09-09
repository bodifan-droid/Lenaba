from __future__ import annotations

import pandas as pd

from scripts.lib.paths import OUTPUTS

OUT = OUTPUTS / "behind_cache.parquet"


def main():

    df = pd.DataFrame(columns=[
        "canonical_name",
        "url",
        "html_hash",
        "fetched_at",
        "parsed_ok",
    ])

    df.to_parquet(OUT, index=False)

    print("=" * 45)
    print("BEHIND CACHE INITIALIZED")
    print("=" * 45)
    print(f"Output : {OUT.name}")


if __name__ == "__main__":
    main()
