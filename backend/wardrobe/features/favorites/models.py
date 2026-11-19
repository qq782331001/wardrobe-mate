"""收藏目标和返回模型。"""

from typing import Literal
from uuid import UUID, uuid4

from pydantic import Field

from wardrobe.models.base import InputModel


TargetType = Literal["item", "outfit"]


class FavoriteInput(InputModel):
    target_type: TargetType
    target_id: UUID


class Favorite(FavoriteInput):
    id: UUID = Field(default_factory=uuid4)
    target_exists: bool = True
