"""主题衣物集合维护。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.collections.models import Collection, CollectionInput
from wardrobe.features.collections.state import collections
from wardrobe.storage.memory import store


def _render(collection: Collection) -> Collection:
    return collection.model_copy(update={
        "missing_item_ids": [item_id for item_id in collection.item_ids if item_id not in store.items],
    })


def _check(payload: CollectionInput) -> None:
    for item_id in payload.item_ids:
        if item_id not in store.items:
            raise HTTPException(status_code=422, detail=f"衣物不存在：{item_id}")


def list_collections() -> list[Collection]:
    """列出集合，保留已经失效的原始单品引用。"""
    return [_render(collection) for collection in collections.values()]


def get_collection(collection_id: UUID) -> Collection:
    collection = collections.get(collection_id)
    if collection is None:
        raise HTTPException(status_code=404, detail="衣物集合不存在")
    return _render(collection)


def create_collection(payload: CollectionInput) -> Collection:
    _check(payload)
    collection = Collection(**payload.model_dump())
    collections[collection.id] = collection
    return _render(collection)


def replace_collection(collection_id: UUID, payload: CollectionInput) -> Collection:
    get_collection(collection_id)
    _check(payload)
    collection = Collection(id=collection_id, **payload.model_dump())
    collections[collection_id] = collection
    return _render(collection)


def delete_collection(collection_id: UUID) -> None:
    """删除集合，不修改衣物记录。"""
    get_collection(collection_id)
    del collections[collection_id]
