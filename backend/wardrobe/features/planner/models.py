"""穿搭计划输入与读取模型。"""

from datetime import date
from uuid import UUID, uuid4

from pydantic import Field

from wardrobe.models.base import InputModel


class PlanInput(InputModel):
    """用户提供日期和已有搭配，不自动生成实际穿着记录。"""

    outfit_id: UUID
    planned_on: date
    occasion: str | None = Field(default=None, max_length=80)
    notes: str | None = Field(default=None, max_length=1000)


class Plan(PlanInput):
    """保存的穿搭计划。"""

    id: UUID = Field(default_factory=uuid4)


class PlanView(Plan):
    """读取时说明关联搭配是否仍存在。"""

    outfit_exists: bool
