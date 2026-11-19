"""搭配组合输入与返回模型。"""

from uuid import UUID, uuid4

from pydantic import Field, field_validator

from wardrobe.models.base import InputModel


class OutfitInput(InputModel):
    """一套搭配引用衣橱中的不同单品。"""

    name: str = Field(min_length=1, max_length=120)
    item_ids: list[UUID] = Field(min_length=1, max_length=30)
    occasion: str | None = Field(default=None, max_length=80)

    @field_validator("item_ids")
    @classmethod
    def reject_duplicate_items(cls, item_ids: list[UUID]) -> list[UUID]:
        """同一套搭配不能重复引用单品。"""
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("同一套搭配不能重复引用单品")
        return item_ids


class Outfit(OutfitInput):
    """带有唯一标识的搭配记录。"""

    id: UUID = Field(default_factory=uuid4)
