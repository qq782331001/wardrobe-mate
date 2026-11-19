"""读取当前内存中的衣橱数据用于导出。"""

from wardrobe.models.export import WardrobeExport
from wardrobe.storage.memory import store


def export_wardrobe() -> WardrobeExport:
    """返回当前衣物、搭配和穿着记录，不修改存储。"""
    return WardrobeExport(
        items=list(store.items.values()),
        outfits=list(store.outfits.values()),
        wear_logs=list(store.wear_logs.values()),
    )
