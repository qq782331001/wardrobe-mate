"""搭配管理接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.models.outfit import Outfit, OutfitInput
from wardrobe.services import outfits as outfit_service


router = APIRouter(prefix="/outfits", tags=["搭配"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_outfit(payload: OutfitInput) -> Outfit:
    """使用当前可用的衣物创建搭配。"""
    return outfit_service.create_outfit(payload)


@router.get("")
async def list_outfits() -> list[Outfit]:
    """列出已保存的搭配。"""
    return outfit_service.list_outfits()


@router.get("/{outfit_id}")
async def get_outfit(outfit_id: UUID) -> Outfit:
    """查看指定搭配。"""
    return outfit_service.get_outfit(outfit_id)


@router.put("/{outfit_id}")
async def replace_outfit(outfit_id: UUID, payload: OutfitInput) -> Outfit:
    """完整更新搭配并重新检查单品状态。"""
    return outfit_service.replace_outfit(outfit_id, payload)


@router.delete("/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_outfit(outfit_id: UUID) -> Response:
    """删除未被穿着记录引用的搭配。"""
    outfit_service.delete_outfit(outfit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
