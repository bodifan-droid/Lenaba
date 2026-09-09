
from __future__ import annotations

import pandas as pd

from scripts.lib.paths import OUTPUTS

OUT = OUTPUTS / "fetch_results.parquet"


def main():

    df = pd.DataFrame(
        columns=[
            "family_id",
            "canonical_name",
            "batch_key",
            "meaning",
            "origin",
            "pronunciation",
            "api_status",
            "fetched_at",
        ]
    )

    df.to_parquet(OUT, index=False)

    print("=" * 45)
    print("FETCH RESULTS INITIALIZED")
    print("=" * 45)
    print(f"Output : {OUT.name}")


if __name__ == "__main__":
    main()
