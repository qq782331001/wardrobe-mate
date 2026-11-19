"""实际穿着日期与个人反馈模型。"""

from datetime import date
from typing import Literal
from uuid import UUID, uuid4

from pydantic import Field

from wardrobe.models.base import InputModel


class WearLogInput(InputModel):
    """记录某套搭配的实际穿着和可选反馈。"""

    outfit_id: UUID
    worn_on: date
    feedback: Literal["liked", "neutral", "disliked"] = "neutral"
    notes: str | None = Field(default=None, max_length=500)


class WearLog(WearLogInput):
    """带有唯一标识的穿着记录。"""

    id: UUID = Field(default_factory=uuid4)
