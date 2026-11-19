"""穿着窗口和当前衣橱的汇总数据。"""

from datetime import date
from uuid import UUID

from wardrobe.models.base import InputModel
from wardrobe.models.category import Category


class WardrobeInsights(InputModel):
    """当前数据在指定日期窗口中的汇总，不代表历史快照。"""

    start_date: date
    end_date: date
    days: int
    wear_log_count: int
    feedback_counts: dict[str, int]
    daily_counts: dict[date, int]
    unworn_item_ids: list[UUID]
    wardrobe_category_counts: dict[Category, int]
    worn_category_counts: dict[Category, int]
