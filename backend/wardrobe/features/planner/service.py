"""穿搭日期安排及日期范围筛选。"""

from datetime import date
from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.planner.models import Plan, PlanInput, PlanView
from wardrobe.features.planner.state import plans
from wardrobe.storage.memory import store


def _record(plan_id: UUID) -> Plan:
    record = plans.get(plan_id)
    if record is None:
        raise HTTPException(status_code=404, detail="穿搭计划不存在")
    return record


def _view(record: Plan) -> PlanView:
    return PlanView(**record.model_dump(), outfit_exists=record.outfit_id in store.outfits)


def _check_outfit(outfit_id: UUID) -> None:
    if outfit_id not in store.outfits:
        raise HTTPException(status_code=422, detail="计划引用的搭配不存在")


def list_plans(start_date: date | None = None, end_date: date | None = None) -> list[PlanView]:
    """按包含边界的日期区间筛选，按计划日期排序。"""
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(status_code=422, detail="开始日期不能晚于结束日期")
    selected = [
        record
        for record in plans.values()
        if (start_date is None or record.planned_on >= start_date)
        and (end_date is None or record.planned_on <= end_date)
    ]
    return [_view(record) for record in sorted(selected, key=lambda plan: (plan.planned_on, str(plan.id)))]


def get_plan(plan_id: UUID) -> PlanView:
    """查看计划及当前关联状态。"""
    return _view(_record(plan_id))


def create_plan(payload: PlanInput) -> PlanView:
    """为已有搭配创建日期安排。"""
    _check_outfit(payload.outfit_id)
    record = Plan(**payload.model_dump())
    plans[record.id] = record
    return _view(record)


def replace_plan(plan_id: UUID, payload: PlanInput) -> PlanView:
    """完整更新计划，日期始终由请求明确提供。"""
    _record(plan_id)
    _check_outfit(payload.outfit_id)
    record = Plan(id=plan_id, **payload.model_dump())
    plans[plan_id] = record
    return _view(record)


def delete_plan(plan_id: UUID) -> None:
    """删除计划，不影响搭配和实际穿着记录。"""
    _record(plan_id)
    del plans[plan_id]
