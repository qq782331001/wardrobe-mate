"""出行清单与装箱状态管理。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.packing_lists.models import PackingList, PackingListInput, PackingListView
from wardrobe.features.packing_lists.state import packing_lists
from wardrobe.storage.memory import store


def _record(list_id: UUID) -> PackingList:
    record = packing_lists.get(list_id)
    if record is None:
        raise HTTPException(status_code=404, detail="行李清单不存在")
    return record


def _view(record: PackingList) -> PackingListView:
    missing = [item_id for item_id in record.item_ids if item_id not in store.items]
    unavailable = [
        item_id
        for item_id in record.item_ids
        if item_id in store.items and not store.items[item_id].available
    ]
    return PackingListView(
        **record.model_dump(),
        missing_item_ids=missing,
        unavailable_item_ids=unavailable,
    )


def _check_items(item_ids: list[UUID]) -> None:
    missing = [item_id for item_id in item_ids if item_id not in store.items]
    if missing:
        raise HTTPException(status_code=422, detail="行李清单包含不存在的衣物")


def list_packing_lists() -> list[PackingListView]:
    """列出所有出行清单及当前衣物状态。"""
    return [_view(record) for record in packing_lists.values()]


def get_packing_list(list_id: UUID) -> PackingListView:
    """查看单个清单。"""
    return _view(_record(list_id))


def create_packing_list(payload: PackingListInput) -> PackingListView:
    """创建清单，允许先计划当前不可用但真实存在的衣物。"""
    _check_items(payload.item_ids)
    record = PackingList(**payload.model_dump())
    packing_lists[record.id] = record
    return _view(record)


def replace_packing_list(list_id: UUID, payload: PackingListInput) -> PackingListView:
    """完整更新清单和装箱状态。"""
    _record(list_id)
    _check_items(payload.item_ids)
    record = PackingList(id=list_id, **payload.model_dump())
    packing_lists[list_id] = record
    return _view(record)


def delete_packing_list(list_id: UUID) -> None:
    """删除清单，不删除衣物。"""
    _record(list_id)
    del packing_lists[list_id]
