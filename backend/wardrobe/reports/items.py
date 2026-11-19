"""衣物明细表导出。"""

from fastapi import Response

from wardrobe.reports.csv_tools import csv_download
from wardrobe.storage.memory import store


def download_items() -> Response:
    """导出衣物的基本属性，不下载图片。"""
    return csv_download(
        "wardrobe-items.csv",
        ["id", "name", "category", "color", "available", "image_url"],
        (
            (
                item.id,
                item.name,
                item.category.value,
                item.color,
                str(item.available).lower(),
                str(item.image_url) if item.image_url is not None else None,
            )
            for item in store.items.values()
        ),
    )
