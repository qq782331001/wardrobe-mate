"""穿着记录与反馈接口。"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.models.wear_log import WearLog, WearLogInput
from wardrobe.services import wear_logs as wear_log_service


router = APIRouter(prefix="/wear-logs", tags=["穿着记录"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_wear_log(payload: WearLogInput) -> WearLog:
    """记录指定日期穿着的搭配和反馈。"""
    return wear_log_service.create_wear_log(payload)


@router.get("")
async def list_wear_logs(
    outfit_id: UUID | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[WearLog]:
    """按搭配和日期范围查询穿着记录。"""
    return wear_log_service.list_wear_logs(
        outfit_id=outfit_id,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{log_id}")
async def get_wear_log(log_id: UUID) -> WearLog:
    """查看指定穿着记录。"""
    return wear_log_service.get_wear_log(log_id)


@router.put("/{log_id}")
async def replace_wear_log(log_id: UUID, payload: WearLogInput) -> WearLog:
    """完整更新穿着记录和反馈。"""
    return wear_log_service.replace_wear_log(log_id, payload)


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wear_log(log_id: UUID) -> Response:
    """删除指定穿着记录。"""
    wear_log_service.delete_wear_log(log_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
