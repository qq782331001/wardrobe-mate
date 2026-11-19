"""备注输入与返回模型。"""

from typing import Literal
from uuid import UUID, uuid4

from pydantic import Field

from wardrobe.models.base import InputModel


TargetType = Literal["item", "outfit"]


class NoteInput(InputModel):
    target_type: TargetType
    target_id: UUID
    content: str = Field(min_length=1, max_length=2000)


class Note(NoteInput):
    id: UUID = Field(default_factory=uuid4)
    target_exists: bool = True
