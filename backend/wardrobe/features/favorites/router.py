"""收藏接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.features.favorites import service
from wardrobe.features.favorites.models import Favorite, FavoriteInput, TargetType


router = APIRouter(prefix="/favorites", tags=["收藏"])


@router.get("")
async def list_favorites(target_type: TargetType | None = None) -> list[Favorite]:
    return service.list_favorites(target_type)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_favorite(payload: FavoriteInput) -> Favorite:
    return service.create_favorite(payload)


@router.get("/{favorite_id}")
async def get_favorite(favorite_id: UUID) -> Favorite:
    return service.get_favorite(favorite_id)


@router.delete("/{favorite_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite(favorite_id: UUID) -> Response:
    service.delete_favorite(favorite_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
