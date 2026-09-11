from __future__ import annotations

import pandas as pd

from scripts.lib.paths import KNOWLEDGE

OUT = KNOWLEDGE / "etymology_graph.parquet"


def main():

    df = pd.DataFrame(columns=[
        "from_name",
        "relation",
        "to_name",
        "target_language",
        "source",
    ])

    df.to_parquet(OUT, index=False)

    print("=" * 45)
    print("ETYMOLOGY GRAPH INITIALIZED")
    print("=" * 45)
    print(f"Output : {OUT.name}")


if __name__ == "__main__":
    main()
