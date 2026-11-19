"""搭配明细表导出。"""

from fastapi import Response

from wardrobe.reports.csv_tools import csv_download
from wardrobe.storage.memory import store


def download_outfits() -> Response:
    """每套搭配占一行，单品标识以分号分隔。"""
    return csv_download(
        "wardrobe-outfits.csv",
        ["id", "name", "occasion", "item_ids"],
        (
            (
                outfit.id,
                outfit.name,
                outfit.occasion,
                ";".join(str(item_id) for item_id in outfit.item_ids),
            )
            for outfit in store.outfits.values()
        ),
    )
