"""汇总指定日期窗口内的穿着记录。"""

from datetime import date

from wardrobe.features.insights.calculations import count_daily, count_feedback, window_bounds
from wardrobe.features.insights.models import WardrobeInsights
from wardrobe.models.category import Category
from wardrobe.storage.memory import store


def get_insights(as_of: date, days: int = 30) -> WardrobeInsights:
    """根据显式日期计算汇总，单品关联使用当前搭配而非历史快照。"""
    start, end = window_bounds(as_of, days)
    logs = [
        log
        for log in store.wear_logs.values()
        if start <= log.worn_on <= end
    ]
    worn_ids = set()
    for log in logs:
        outfit = store.outfits.get(log.outfit_id)
        if outfit is not None:
            worn_ids.update(item_id for item_id in outfit.item_ids if item_id in store.items)
    wardrobe_counts = {category: 0 for category in Category}
    worn_counts = {category: 0 for category in Category}
    for item in store.items.values():
        wardrobe_counts[item.category] += 1
        if item.id in worn_ids:
            worn_counts[item.category] += 1
    return WardrobeInsights(
        start_date=start,
        end_date=end,
        days=(end - start).days + 1,
        wear_log_count=len(logs),
        feedback_counts=count_feedback(logs),
        daily_counts=count_daily(logs, start, end),
        unworn_item_ids=sorted(set(store.items) - worn_ids, key=str),
        wardrobe_category_counts=wardrobe_counts,
        worn_category_counts=worn_counts,
    )
