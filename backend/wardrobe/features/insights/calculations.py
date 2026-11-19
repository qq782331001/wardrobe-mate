"""日期窗口与穿着反馈的纯计算函数。"""

from datetime import date

from wardrobe.models.wear_log import WearLog


def window_bounds(as_of: date, days: int) -> tuple[date, date]:
    """返回含结束日的日期窗口，在日期类型的最小值处截断。"""
    start_ordinal = max(date.min.toordinal(), as_of.toordinal() - days + 1)
    return date.fromordinal(start_ordinal), as_of


def count_feedback(logs: list[WearLog]) -> dict[str, int]:
    """保留全部约定反馈键，即使某种反馈尚未出现。"""
    counts = {"liked": 0, "neutral": 0, "disliked": 0}
    for log in logs:
        counts[log.feedback] += 1
    return counts


def count_daily(logs: list[WearLog], start: date, end: date) -> dict[date, int]:
    """逐日计数，窗口内无穿着记录的日期返回零。"""
    counts = {
        date.fromordinal(ordinal): 0
        for ordinal in range(start.toordinal(), end.toordinal() + 1)
    }
    for log in logs:
        if start <= log.worn_on <= end:
            counts[log.worn_on] += 1
    return counts
