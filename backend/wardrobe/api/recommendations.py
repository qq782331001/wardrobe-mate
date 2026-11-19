"""已保存搭配的基础规则推荐接口。"""

from fastapi import APIRouter

from wardrobe.models.recommendation import RecommendationRequest, RecommendationResult
from wardrobe.services import recommendations as recommendation_service


router = APIRouter(prefix="/recommendations", tags=["推荐"])


@router.post("")
async def recommend_outfits(payload: RecommendationRequest) -> RecommendationResult:
    """按场景、锁定单品及穿着次数筛选已保存的搭配。"""
    return recommendation_service.recommend_outfits(payload)
