"""待购意向管理，不写入真实衣橱。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.wishlist.models import Wish, WishInput
from wardrobe.features.wishlist.state import wishes
from wardrobe.models.category import Category


def get_wish(wish_id: UUID) -> Wish:
    """获取指定待购意向。"""
    wish = wishes.get(wish_id)
    if wish is None:
        raise HTTPException(status_code=404, detail="待购意向不存在")
    return wish


def list_wishes(category: Category | None = None, priority: str | None = None) -> list[Wish]:
    """按分类和优先级筛选待购意向。"""
    return [
        wish
        for wish in wishes.values()
        if (category is None or wish.category == category)
        and (priority is None or wish.priority == priority)
    ]


def create_wish(payload: WishInput) -> Wish:
    """保存待购意向，不访问商品地址。"""
    wish = Wish(**payload.model_dump())
    wishes[wish.id] = wish
    return wish


def replace_wish(wish_id: UUID, payload: WishInput) -> Wish:
    """完整更新待购意向。"""
    get_wish(wish_id)
    wish = Wish(id=wish_id, **payload.model_dump())
    wishes[wish_id] = wish
    return wish


def delete_wish(wish_id: UUID) -> None:
    """移除待购意向，不影响真实衣物。"""
    get_wish(wish_id)
    del wishes[wish_id]
