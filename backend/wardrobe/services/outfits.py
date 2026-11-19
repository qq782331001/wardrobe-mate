"""搭配保存与单品引用管理。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.models.outfit import Outfit, OutfitInput
from wardrobe.storage.memory import store


def check_outfit_items(item_ids: list[UUID]) -> None:
    """确认引用的衣物存在且当前可用。"""
    for item_id in item_ids:
        item = store.items.get(item_id)
        if item is None:
            raise HTTPException(status_code=422, detail=f"衣物不存在：{item_id}")
        if not item.available:
            raise HTTPException(status_code=422, detail=f"衣物当前不可用：{item_id}")


def list_outfits() -> list[Outfit]:
    """返回已保存搭配，保留后来包含不可用衣物的搭配。"""
    return list(store.outfits.values())


def get_outfit(outfit_id: UUID) -> Outfit:
    """获取搭配，不存在时返回资源错误。"""
    outfit = store.outfits.get(outfit_id)
    if outfit is None:
        raise HTTPException(status_code=404, detail="搭配不存在")
    return outfit


def create_outfit(payload: OutfitInput) -> Outfit:
    """使用衣橱中当前可用的衣物保存搭配。"""
    check_outfit_items(payload.item_ids)
    outfit = Outfit(**payload.model_dump())
    store.outfits[outfit.id] = outfit
    return outfit


def replace_outfit(outfit_id: UUID, payload: OutfitInput) -> Outfit:
    """完整更新搭配，重新检查单品引用和可用状态。"""
    get_outfit(outfit_id)
    check_outfit_items(payload.item_ids)
    outfit = Outfit(id=outfit_id, **payload.model_dump())
    store.outfits[outfit_id] = outfit
    return outfit


def delete_outfit(outfit_id: UUID) -> None:
    """删除未被穿着记录引用的搭配。"""
    get_outfit(outfit_id)
    if any(log.outfit_id == outfit_id for log in store.wear_logs.values()):
        raise HTTPException(
            status_code=409,
            detail="搭配仍被穿着记录引用，请先删除相关穿着记录",
        )
    del store.outfits[outfit_id]
