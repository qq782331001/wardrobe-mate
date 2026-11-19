"""根据实际衣橱与穿着记录汇总统计。"""

from collections import Counter
from uuid import UUID

from wardrobe.models.category import Category
from wardrobe.models.statistics import ItemWearCount, WardrobeStats
from wardrobe.storage.memory import store


def wardrobe_statistics() -> WardrobeStats:
    """汇总衣物分类、可用数量及按穿着记录计算的单品使用次数。"""
    category_counts = {category: 0 for category in Category}
    for item in store.items.values():
        category_counts[item.category] += 1

    wear_counts: Counter[UUID] = Counter()
    for log in store.wear_logs.values():
        outfit = store.outfits.get(log.outfit_id)
        if outfit is not None:
            wear_counts.update(outfit.item_ids)

    most_worn_items = [
        ItemWearCount(item_id=item.id, name=item.name, wear_count=wear_counts[item.id])
        for item in store.items.values()
    ]
    most_worn_items.sort(
        key=lambda item: (-item.wear_count, item.name.casefold(), str(item.item_id))
    )
    return WardrobeStats(
        total_items=len(store.items),
        available_items=sum(item.available for item in store.items.values()),
        total_outfits=len(store.outfits),
        total_wear_logs=len(store.wear_logs),
        category_counts=category_counts,
        most_worn_items=most_worn_items,
    )
