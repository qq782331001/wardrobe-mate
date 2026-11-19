"""衣橱数量与单品穿着次数统计模型。"""

from uuid import UUID

from pydantic import BaseModel

from wardrobe.models.category import Category


class ItemWearCount(BaseModel):
    """一件衣物在实际穿着记录中出现的次数。"""

    item_id: UUID
    name: str
    wear_count: int


class WardrobeStats(BaseModel):
    """衣橱、搭配和穿着记录的汇总。"""

    total_items: int
    available_items: int
    total_outfits: int
    total_wear_logs: int
    category_counts: dict[Category, int]
    most_worn_items: list[ItemWearCount]
