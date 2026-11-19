"""穿着记录和反馈管理。"""

from datetime import date
from uuid import UUID

from fastapi import HTTPException

from wardrobe.models.wear_log import WearLog, WearLogInput
from wardrobe.services.outfits import check_outfit_items, get_outfit
from wardrobe.storage.memory import store


def list_wear_logs(
    outfit_id: UUID | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[WearLog]:
    """按搭配及包含边界的日期范围查询，最近穿着记录优先。"""
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(status_code=422, detail="开始日期不能晚于结束日期")
    records = [
        log
        for log in store.wear_logs.values()
        if (outfit_id is None or log.outfit_id == outfit_id)
        and (start_date is None or log.worn_on >= start_date)
        and (end_date is None or log.worn_on <= end_date)
    ]
    return sorted(records, key=lambda log: (log.worn_on, str(log.id)), reverse=True)


def get_wear_log(log_id: UUID) -> WearLog:
    """获取指定穿着记录。"""
    log = store.wear_logs.get(log_id)
    if log is None:
        raise HTTPException(status_code=404, detail="穿着记录不存在")
    return log


def create_wear_log(payload: WearLogInput) -> WearLog:
    """为存在且单品当前可用的搭配新增穿着记录。"""
    outfit = get_outfit(payload.outfit_id)
    check_outfit_items(outfit.item_ids)
    log = WearLog(**payload.model_dump())
    store.wear_logs[log.id] = log
    return log


def replace_wear_log(log_id: UUID, payload: WearLogInput) -> WearLog:
    """完整更新穿着记录，检查更新后的搭配和单品。"""
    get_wear_log(log_id)
    outfit = get_outfit(payload.outfit_id)
    check_outfit_items(outfit.item_ids)
    log = WearLog(id=log_id, **payload.model_dump())
    store.wear_logs[log_id] = log
    return log


def delete_wear_log(log_id: UUID) -> None:
    """删除穿着记录，保留对应搭配和衣物。"""
    get_wear_log(log_id)
    del store.wear_logs[log_id]
