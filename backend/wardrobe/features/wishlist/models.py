"""待购衣物的输入和返回模型。"""

from decimal import Decimal
from typing import Literal
from uuid import UUID, uuid4

from pydantic import Field, HttpUrl

from wardrobe.models.base import InputModel
from wardrobe.models.category import Category


class WishInput(InputModel):
    """记录待购意向，不代表已经拥有的衣物。"""

    name: str = Field(min_length=1, max_length=120)
    category: Category
    color: str | None = Field(default=None, max_length=40)
    product_url: HttpUrl | None = None
    budget: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)
    priority: Literal["low", "normal", "high"] = "normal"
    notes: str | None = Field(default=None, max_length=1000)


class Wish(WishInput):
    """带有唯一标识的待购意向。"""

    id: UUID = Field(default_factory=uuid4)
