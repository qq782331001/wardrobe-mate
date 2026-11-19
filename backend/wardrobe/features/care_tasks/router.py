"""衣物护理任务接口。"""

from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Response

from wardrobe.features.care_tasks import service
from wardrobe.features.care_tasks.models import CareTaskInput, CareTaskView


router = APIRouter(prefix="/care-tasks", tags=["护理任务"])


@router.post("", status_code=201)
async def create_task(payload: CareTaskInput) -> CareTaskView:
    """新增护理任务。"""
    return service.create_task(payload)


@router.get("")
async def list_tasks(status: Literal["pending", "done"] | None = None) -> list[CareTaskView]:
    """查看护理任务，可按状态筛选。"""
    return service.list_tasks(status=status)


@router.get("/{task_id}")
async def get_task(task_id: UUID) -> CareTaskView:
    """查看指定任务。"""
    return service.get_task(task_id)


@router.put("/{task_id}")
async def replace_task(task_id: UUID, payload: CareTaskInput) -> CareTaskView:
    """完整更新护理任务。"""
    return service.replace_task(task_id, payload)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: UUID) -> Response:
    """删除护理任务。"""
    service.delete_task(task_id)
    return Response(status_code=204)
