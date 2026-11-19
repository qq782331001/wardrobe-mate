"""保存布局并标明衣物与搭配的实时引用状态。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.canvas.models import CanvasDocument, CanvasInput
from wardrobe.features.canvas.state import canvases
from wardrobe.storage.memory import store


def build_document(outfit_id: UUID, layout: CanvasInput) -> CanvasDocument:
    """核心资源删除或变更后保留布局，同时明确显示失效图层。"""
    outfit = store.outfits.get(outfit_id)
    outfit_items = set(outfit.item_ids) if outfit is not None else set()
    missing: list[UUID] = []
    unavailable: list[UUID] = []
    for layer in layout.layers:
        item = store.items.get(layer.item_id)
        if item is None or layer.item_id not in outfit_items:
            missing.append(layer.item_id)
        if item is not None and not item.available:
            unavailable.append(layer.item_id)
    return CanvasDocument(
        **layout.model_dump(),
        outfit_id=outfit_id,
        outfit_exists=outfit is not None,
        missing_item_ids=missing,
        unavailable_item_ids=unavailable,
    )


def get_canvas(outfit_id: UUID) -> CanvasDocument:
    """读取已有布局，即使核心搭配后来被删除也不隐藏失效状态。"""
    layout = canvases.get(outfit_id)
    if layout is None:
        raise HTTPException(status_code=404, detail="画布布局不存在")
    return build_document(outfit_id, layout)


def replace_canvas(outfit_id: UUID, payload: CanvasInput) -> CanvasDocument:
    """创建或完整替换布局，所有图层必须属于当前真实搭配。"""
    outfit = store.outfits.get(outfit_id)
    if outfit is None:
        raise HTTPException(status_code=422, detail="搭配不存在，不能保存画布")
    allowed_items = set(outfit.item_ids)
    for layer in payload.layers:
        if layer.item_id not in store.items:
            raise HTTPException(status_code=422, detail=f"衣物不存在：{layer.item_id}")
        if layer.item_id not in allowed_items:
            raise HTTPException(status_code=422, detail=f"衣物不属于当前搭配：{layer.item_id}")
    canvases[outfit_id] = payload.model_copy(deep=True)
    return build_document(outfit_id, canvases[outfit_id])


def delete_canvas(outfit_id: UUID) -> None:
    """仅删除布局，不修改搭配或衣物。"""
    if outfit_id not in canvases:
        raise HTTPException(status_code=404, detail="画布布局不存在")
    del canvases[outfit_id]
