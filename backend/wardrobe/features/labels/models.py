"""自定义标签的输入与返回模型。"""

from uuid import UUID, uuid4

from pydantic import Field, field_validator

from wardrobe.models.base import InputModel


class LabelInput(InputModel):
    name: str = Field(min_length=1, max_length=80)
    color: str | None = Field(default=None, pattern=r"^#[0-9A-Fa-f]{6}$")
    item_ids: list[UUID] = Field(default_factory=list, max_length=200)

    @field_validator("item_ids")
    @classmethod
    def unique_items(cls, item_ids: list[UUID]) -> list[UUID]:
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("标签关联的衣物不能重复")
        return item_ids


class Label(LabelInput):
    id: UUID = Field(default_factory=uuid4)
    missing_item_ids: list[UUID] = Field(default_factory=list)
