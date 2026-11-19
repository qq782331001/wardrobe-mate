"""衣物集合接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.features.collections import service
from wardrobe.features.collections.models import Collection, CollectionInput


router = APIRouter(prefix="/collections", tags=["衣物集合"])


@router.get("")
async def list_collections() -> list[Collection]:
    return service.list_collections()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_collection(payload: CollectionInput) -> Collection:
    return service.create_collection(payload)


@router.get("/{collection_id}")
async def get_collection(collection_id: UUID) -> Collection:
    return service.get_collection(collection_id)


@router.put("/{collection_id}")
async def replace_collection(collection_id: UUID, payload: CollectionInput) -> Collection:
    return service.replace_collection(collection_id, payload)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection(collection_id: UUID) -> Response:
    service.delete_collection(collection_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
