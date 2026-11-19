"""衣物集合的数据模型。"""

from uuid import UUID, uuid4

from pydantic import Field, field_validator

from wardrobe.models.base import InputModel


class CollectionInput(InputModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    item_ids: list[UUID] = Field(default_factory=list, max_length=200)

    @field_validator("item_ids")
    @classmethod
    def unique_items(cls, item_ids: list[UUID]) -> list[UUID]:
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("集合内不能重复添加同一件衣物")
        return item_ids


class Collection(CollectionInput):
    id: UUID = Field(default_factory=uuid4)
    missing_item_ids: list[UUID] = Field(default_factory=list)
