"""收藏保存与目标存续状态查询。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.favorites.models import Favorite, FavoriteInput, TargetType
from wardrobe.features.favorites.state import favorites
from wardrobe.storage.memory import store


def _target_exists(target_type: TargetType, target_id: UUID) -> bool:
    return target_id in (store.items if target_type == "item" else store.outfits)


def _render(favorite: Favorite) -> Favorite:
    return favorite.model_copy(update={
        "target_exists": _target_exists(favorite.target_type, favorite.target_id),
    })


def list_favorites(target_type: TargetType | None = None) -> list[Favorite]:
    return [_render(favorite) for favorite in favorites.values()
            if target_type is None or favorite.target_type == target_type]


def get_favorite(favorite_id: UUID) -> Favorite:
    favorite = favorites.get(favorite_id)
    if favorite is None:
        raise HTTPException(status_code=404, detail="收藏不存在")
    return _render(favorite)


def create_favorite(payload: FavoriteInput) -> Favorite:
    """收藏已有衣物或搭配，同一目标不能重复收藏。"""
    if not _target_exists(payload.target_type, payload.target_id):
        raise HTTPException(status_code=422, detail="收藏目标不存在")
    if any(favorite.target_type == payload.target_type and favorite.target_id == payload.target_id
           for favorite in favorites.values()):
        raise HTTPException(status_code=409, detail="该目标已收藏")
    favorite = Favorite(**payload.model_dump())
    favorites[favorite.id] = favorite
    return _render(favorite)


def delete_favorite(favorite_id: UUID) -> None:
    """取消收藏，不删除对应衣物或搭配。"""
    get_favorite(favorite_id)
    del favorites[favorite_id]
