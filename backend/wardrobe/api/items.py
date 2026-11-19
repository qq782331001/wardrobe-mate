"""衣物管理接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.models.category import Category
from wardrobe.models.item import Item, ItemInput
from wardrobe.services import items as item_service


router = APIRouter(prefix="/items", tags=["衣物"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemInput) -> Item:
    """新增衣物。"""
    return item_service.create_item(payload)


@router.get("")
async def list_items(
    category: Category | None = None,
    available: bool | None = None,
) -> list[Item]:
    """按分类和可用状态查询衣物。"""
    return item_service.list_items(category=category, available=available)


@router.get("/{item_id}")
async def get_item(item_id: UUID) -> Item:
    """查看指定衣物。"""
    return item_service.get_item(item_id)


@router.put("/{item_id}")
async def replace_item(item_id: UUID, payload: ItemInput) -> Item:
    """完整更新衣物信息。"""
    return item_service.replace_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID) -> Response:
    """删除未被搭配引用的衣物。"""
    item_service.delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
