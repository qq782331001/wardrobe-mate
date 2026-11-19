"""供客户端显示的衣物分类选项。"""

from pydantic import BaseModel

from wardrobe.models.category import Category


class CategoryOption(BaseModel):
    """分类代码及其显示名称。"""

    value: Category
    label: str
