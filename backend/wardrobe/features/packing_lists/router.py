"""行李清单接口。"""

from uuid import UUID

from fastapi import APIRouter, Response

from wardrobe.features.packing_lists import service
from wardrobe.features.packing_lists.models import PackingListInput, PackingListView


router = APIRouter(prefix="/packing-lists", tags=["行李清单"])


@router.post("", status_code=201)
async def create_packing_list(payload: PackingListInput) -> PackingListView:
    """新增出行清单。"""
    return service.create_packing_list(payload)


@router.get("")
async def list_packing_lists() -> list[PackingListView]:
    """列出出行清单。"""
    return service.list_packing_lists()


@router.get("/{list_id}")
async def get_packing_list(list_id: UUID) -> PackingListView:
    """查看指定清单。"""
    return service.get_packing_list(list_id)


@router.put("/{list_id}")
async def replace_packing_list(list_id: UUID, payload: PackingListInput) -> PackingListView:
    """完整更新清单和装箱记录。"""
    return service.replace_packing_list(list_id, payload)


@router.delete("/{list_id}", status_code=204)
async def delete_packing_list(list_id: UUID) -> Response:
    """删除清单。"""
    service.delete_packing_list(list_id)
    return Response(status_code=204)
