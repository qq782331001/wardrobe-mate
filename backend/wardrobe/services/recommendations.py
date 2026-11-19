"""仅基于已保存搭配提供可解释的基础筛选。"""

from collections import Counter

from wardrobe.models.recommendation import (
    RecommendationCandidate,
    RecommendationRequest,
    RecommendationResult,
)
from wardrobe.services.outfits import check_outfit_items
from wardrobe.storage.memory import store


def recommend_outfits(payload: RecommendationRequest) -> RecommendationResult:
    """筛选可用搭配，满足场景与锁定条件，并优先展示穿着次数较少者。"""
    check_outfit_items(payload.locked_item_ids)
    locked_ids = set(payload.locked_item_ids)
    occasion = (payload.occasion or "").strip().casefold()
    wear_counts = Counter(log.outfit_id for log in store.wear_logs.values())
    candidates: list[RecommendationCandidate] = []

    for outfit in store.outfits.values():
        if not locked_ids.issubset(outfit.item_ids):
            continue
        if occasion and (outfit.occasion or "").strip().casefold() != occasion:
            continue
        if any(
            item_id not in store.items or not store.items[item_id].available
            for item_id in outfit.item_ids
        ):
            continue

        wear_count = wear_counts[outfit.id]
        reasons = ["所有单品均在衣橱中且当前可用", f"已记录穿着 {wear_count} 次"]
        if occasion:
            reasons.append("符合所选场景")
        if locked_ids:
            reasons.append("包含全部锁定单品")
        candidates.append(
            RecommendationCandidate(
                outfit=outfit,
                wear_count=wear_count,
                reasons=reasons,
            )
        )

    candidates.sort(
        key=lambda candidate: (
            candidate.wear_count,
            candidate.outfit.name.casefold(),
            str(candidate.outfit.id),
        )
    )
    if not candidates:
        message = (
            "请先保存搭配，再请求推荐"
            if not store.outfits
            else "没有满足场景、锁定单品和衣物可用条件的已保存搭配"
        )
        return RecommendationResult(candidates=[], message=message)
    return RecommendationResult(candidates=candidates[: payload.limit])
