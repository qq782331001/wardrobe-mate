"""衣物与搭配的纯文本搜索接口。"""

from fastapi import APIRouter, Query

from wardrobe.features.search import service
from wardrobe.features.search.models import SearchResult


router = APIRouter(prefix="/search", tags=["文本搜索"])


@router.get("")
async def search(
    q: str = Query(min_length=1, max_length=120),
    limit: int = Query(default=20, ge=1, le=100),
) -> SearchResult:
    """搜索当前衣橱，每种资源分别最多返回 limit 条。"""
    return service.search(q=q, limit=limit)
