"""衣物录入与返回模型。"""

from uuid import UUID, uuid4

from pydantic import Field, HttpUrl

from wardrobe.models.base import InputModel
from wardrobe.models.category import Category


class ItemInput(InputModel):
    """新增或完整更新一件衣物，图片地址仅作为引用。"""

    name: str = Field(min_length=1, max_length=120)
    category: Category
    color: str | None = Field(default=None, max_length=40)
    image_url: HttpUrl | None = None
    available: bool = True


class Item(ItemInput):
    """带有唯一标识的衣物记录。"""

    id: UUID = Field(default_factory=uuid4)
