"""指定窗口的穿着洞察接口。"""

from datetime import date

from fastapi import APIRouter, Query

from wardrobe.features.insights import service
from wardrobe.features.insights.models import WardrobeInsights


router = APIRouter(prefix="/insights", tags=["穿着洞察"])


@router.get("")
async def get_insights(
    as_of: date,
    days: int = Query(default=30, ge=1, le=365),
) -> WardrobeInsights:
    """调用方明确提供结束日，不使用服务器的当前日期。"""
    return service.get_insights(as_of=as_of, days=days)
