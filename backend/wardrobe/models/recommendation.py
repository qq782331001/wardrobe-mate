"""已保存搭配的规则推荐输入与结果。"""

from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from wardrobe.models.base import InputModel
from wardrobe.models.outfit import Outfit


class RecommendationRequest(InputModel):
    """按场景与锁定单品筛选现有搭配。"""

    occasion: str | None = Field(default=None, max_length=80)
    locked_item_ids: list[UUID] = Field(default_factory=list, max_length=30)
    limit: int = Field(default=3, ge=1, le=10)

    @field_validator("locked_item_ids")
    @classmethod
    def reject_duplicate_items(cls, item_ids: list[UUID]) -> list[UUID]:
        """锁定单品只能出现一次。"""
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("锁定单品不能重复")
        return item_ids


class RecommendationCandidate(BaseModel):
    """一套候选搭配及其已有穿着次数和规则说明。"""

    outfit: Outfit
    wear_count: int
    reasons: list[str]


class RecommendationResult(BaseModel):
    """规则推荐结果，候选不足时可附带说明。"""

    candidates: list[RecommendationCandidate]
    message: str | None = None
