"""护理任务管理，仅记录安排，不修改衣物状态。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.care_tasks.models import CareTask, CareTaskInput, CareTaskView
from wardrobe.features.care_tasks.state import tasks
from wardrobe.storage.memory import store


def _record(task_id: UUID) -> CareTask:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="护理任务不存在")
    return task


def _view(task: CareTask) -> CareTaskView:
    return CareTaskView(**task.model_dump(), item_exists=task.item_id in store.items)


def _check_item(item_id: UUID) -> None:
    if item_id not in store.items:
        raise HTTPException(status_code=422, detail="护理任务关联的衣物不存在")


def list_tasks(status: str | None = None) -> list[CareTaskView]:
    """按护理状态筛选，保留已经失去衣物引用的任务。"""
    return [_view(task) for task in tasks.values() if status is None or task.status == status]


def get_task(task_id: UUID) -> CareTaskView:
    """查看任务及其衣物引用是否仍有效。"""
    return _view(_record(task_id))


def create_task(payload: CareTaskInput) -> CareTaskView:
    """为真实衣物安排护理任务。"""
    _check_item(payload.item_id)
    task = CareTask(**payload.model_dump())
    tasks[task.id] = task
    return _view(task)


def replace_task(task_id: UUID, payload: CareTaskInput) -> CareTaskView:
    """完整更新任务，重新检查衣物引用。"""
    _record(task_id)
    _check_item(payload.item_id)
    task = CareTask(id=task_id, **payload.model_dump())
    tasks[task_id] = task
    return _view(task)


def delete_task(task_id: UUID) -> None:
    """删除任务，保留衣物本身。"""
    _record(task_id)
    del tasks[task_id]
