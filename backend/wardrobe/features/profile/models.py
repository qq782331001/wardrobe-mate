"""本地演示用户的偏好数据。"""

from typing import Annotated

from pydantic import Field, StringConstraints, field_validator

from wardrobe.models.base import InputModel
from wardrobe.models.category import Category


StyleName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=40),
]


class ProfilePreferences(InputModel):
    """仅保存本地偏好，不表示已经存在用户账号。"""

    display_name: str = Field(default="本地用户", min_length=1, max_length=80)
    preferred_styles: list[StyleName] = Field(default_factory=list, max_length=20)
    disliked_categories: list[Category] = Field(default_factory=list, max_length=6)
    notes: str | None = Field(default=None, max_length=1000)

    @field_validator("preferred_styles")
    @classmethod
    def unique_styles(cls, values: list[str]) -> list[str]:
        """忽略大小写去重，保留第一次填写的风格名称。"""
        unique: dict[str, str] = {}
        for value in values:
            unique.setdefault(value.casefold(), value)
        return list(unique.values())

    @field_validator("disliked_categories")
    @classmethod
    def unique_categories(cls, values: list[Category]) -> list[Category]:
        """保留输入顺序，去掉重复分类。"""
        return list(dict.fromkeys(values))
