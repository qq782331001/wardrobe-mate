"""衣物基础管理。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.models.category import Category
from wardrobe.models.item import Item, ItemInput
from wardrobe.storage.memory import store


def list_items(
    category: Category | None = None,
    available: bool | None = None,
) -> list[Item]:
    """按分类和可用状态筛选衣物。"""
    return [
        item
        for item in store.items.values()
        if (category is None or item.category == category)
        and (available is None or item.available == available)
    ]


def get_item(item_id: UUID) -> Item:
    """获取衣物，不存在时返回资源错误。"""
    item = store.items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="衣物不存在")
    return item


def create_item(payload: ItemInput) -> Item:
    """新增衣物，仅保存图片地址，不访问图片资源。"""
    item = Item(**payload.model_dump())
    store.items[item.id] = item
    return item


def replace_item(item_id: UUID, payload: ItemInput) -> Item:
    """完整更新衣物，保留原单品标识。"""
    get_item(item_id)
    item = Item(id=item_id, **payload.model_dump())
    store.items[item_id] = item
    return item


def delete_item(item_id: UUID) -> None:
    """删除未被搭配引用的衣物。"""
    get_item(item_id)
    if any(item_id in outfit.item_ids for outfit in store.outfits.values()):
        raise HTTPException(
            status_code=409,
            detail="衣物仍被搭配引用，请先修改或删除相关搭配",
        )
    del store.items[item_id]
