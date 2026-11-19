"""衣物护理任务的输入、保存和展示模型。"""

from datetime import date
from typing import Literal
from uuid import UUID, uuid4

from pydantic import Field

from wardrobe.models.base import InputModel


class CareTaskInput(InputModel):
    """安排护理，不自动改变衣物可用状态。"""

    item_id: UUID
    kind: Literal["wash", "dry_clean", "repair"]
    status: Literal["pending", "done"] = "pending"
    due_on: date | None = None
    notes: str | None = Field(default=None, max_length=1000)


class CareTask(CareTaskInput):
    """保存的护理任务。"""

    id: UUID = Field(default_factory=uuid4)


class CareTaskView(CareTask):
    """读取时同时说明衣物是否仍存在。"""

    item_exists: bool
