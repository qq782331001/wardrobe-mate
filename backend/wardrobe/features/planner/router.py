"""穿搭计划接口。"""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Response

from wardrobe.features.planner import service
from wardrobe.features.planner.models import PlanInput, PlanView


router = APIRouter(prefix="/planner", tags=["穿搭计划"])


@router.post("", status_code=201)
async def create_plan(payload: PlanInput) -> PlanView:
    """新增穿搭计划。"""
    return service.create_plan(payload)


@router.get("")
async def list_plans(start_date: date | None = None, end_date: date | None = None) -> list[PlanView]:
    """按日期范围查看计划。"""
    return service.list_plans(start_date=start_date, end_date=end_date)


@router.get("/{plan_id}")
async def get_plan(plan_id: UUID) -> PlanView:
    """查看指定计划。"""
    return service.get_plan(plan_id)


@router.put("/{plan_id}")
async def replace_plan(plan_id: UUID, payload: PlanInput) -> PlanView:
    """完整更新穿搭安排。"""
    return service.replace_plan(plan_id, payload)


@router.delete("/{plan_id}", status_code=204)
async def delete_plan(plan_id: UUID) -> Response:
    """删除计划。"""
    service.delete_plan(plan_id)
    return Response(status_code=204)
