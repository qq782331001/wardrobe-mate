"""待购愿望清单接口。"""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Response

from wardrobe.features.wishlist import service
from wardrobe.features.wishlist.models import Wish, WishInput
from wardrobe.models.category import Category


router = APIRouter(prefix="/wishlist", tags=["愿望清单"])


@router.post("", status_code=201)
async def create_wish(payload: WishInput) -> Wish:
    """新增待购意向。"""
    return service.create_wish(payload)


@router.get("")
async def list_wishes(
    category: Category | None = None,
    priority: Literal["low", "normal", "high"] | None = None,
) -> list[Wish]:
    """筛选待购意向。"""
    return service.list_wishes(category=category, priority=priority)


@router.get("/{wish_id}")
async def get_wish(wish_id: UUID) -> Wish:
    """查看指定待购意向。"""
    return service.get_wish(wish_id)


@router.put("/{wish_id}")
async def replace_wish(wish_id: UUID, payload: WishInput) -> Wish:
    """完整更新待购意向。"""
    return service.replace_wish(wish_id, payload)


@router.delete("/{wish_id}", status_code=204)
async def delete_wish(wish_id: UUID) -> Response:
    """删除待购意向。"""
    service.delete_wish(wish_id)
    return Response(status_code=204)
