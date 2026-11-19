"""从当前进程的核心数据中搜索衣物与搭配。"""

from fastapi import HTTPException

from wardrobe.features.search.matching import contains_query, normalize_query
from wardrobe.features.search.models import SearchResult
from wardrobe.storage.memory import store


def search(q: str, limit: int = 20) -> SearchResult:
    """按名称、颜色和场景做不区分大小写的子串匹配。"""
    query = normalize_query(q)
    if not query:
        raise HTTPException(status_code=422, detail="搜索关键字不能为空白")
    matched_items = sorted(
        (
            item
            for item in store.items.values()
            if contains_query(query, item.name, item.color)
        ),
        key=lambda item: (item.name.casefold(), str(item.id)),
    )
    matched_outfits = sorted(
        (
            outfit
            for outfit in store.outfits.values()
            if contains_query(query, outfit.name, outfit.occasion)
        ),
        key=lambda outfit: (outfit.name.casefold(), str(outfit.id)),
    )
    return SearchResult(
        items=matched_items[:limit],
        outfits=matched_outfits[:limit],
        item_total=len(matched_items),
        outfit_total=len(matched_outfits),
    )
