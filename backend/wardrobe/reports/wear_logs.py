"""穿着记录表导出。"""

from fastapi import Response

from wardrobe.reports.csv_tools import csv_download
from wardrobe.storage.memory import store


def download_wear_logs() -> Response:
    """导出记录本身，不展开当前搭配或推测历史衣物。"""
    return csv_download(
        "wardrobe-wear-logs.csv",
        ["id", "outfit_id", "worn_on", "feedback", "notes"],
        (
            (
                log.id,
                log.outfit_id,
                log.worn_on.isoformat(),
                log.feedback,
                log.notes,
            )
            for log in store.wear_logs.values()
        ),
    )
