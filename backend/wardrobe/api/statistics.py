"""衣橱和穿着情况统计接口。"""

from fastapi import APIRouter

from wardrobe.models.statistics import WardrobeStats
from wardrobe.services import statistics as statistics_service


router = APIRouter(prefix="/statistics", tags=["统计"])


@router.get("")
async def wardrobe_statistics() -> WardrobeStats:
    """汇总衣物、搭配、记录数量及单品穿着次数。"""
    return statistics_service.wardrobe_statistics()
