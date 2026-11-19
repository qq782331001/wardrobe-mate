"""行李清单输入与展示模型。"""

from datetime import date
from uuid import UUID, uuid4

from pydantic import Field, model_validator

from wardrobe.models.base import InputModel


class PackingListInput(InputModel):
    """出行日期、计划携带衣物与已装箱衣物。"""

    name: str = Field(min_length=1, max_length=120)
    destination: str | None = Field(default=None, max_length=120)
    start_date: date | None = None
    end_date: date | None = None
    item_ids: list[UUID] = Field(default_factory=list, max_length=200)
    packed_item_ids: list[UUID] = Field(default_factory=list, max_length=200)

    @model_validator(mode="after")
    def check_content(self) -> "PackingListInput":
        """限制日期顺序和装箱项目的集合关系。"""
        if self.start_date is not None and self.end_date is not None:
            if self.start_date > self.end_date:
                raise ValueError("出发日期不能晚于结束日期")
        if len(self.item_ids) != len(set(self.item_ids)):
            raise ValueError("行李清单不能重复引用衣物")
        if len(self.packed_item_ids) != len(set(self.packed_item_ids)):
            raise ValueError("已装箱衣物不能重复")
        if not set(self.packed_item_ids).issubset(self.item_ids):
            raise ValueError("已装箱衣物必须属于行李清单")
        return self


class PackingList(PackingListInput):
    """保存的出行清单。"""

    id: UUID = Field(default_factory=uuid4)


class PackingListView(PackingList):
    """同时展示失效或当前不可用的衣物引用。"""

    missing_item_ids: list[UUID]
    unavailable_item_ids: list[UUID]
