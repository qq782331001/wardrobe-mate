"""标签维护及衣物引用检查。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.labels.models import Label, LabelInput
from wardrobe.features.labels.state import labels
from wardrobe.storage.memory import store


def _render(label: Label) -> Label:
    return label.model_copy(update={
        "missing_item_ids": [item_id for item_id in label.item_ids if item_id not in store.items],
    })


def _check(payload: LabelInput, exclude_id: UUID | None = None) -> None:
    if any(label.id != exclude_id and label.name.casefold() == payload.name.casefold()
           for label in labels.values()):
        raise HTTPException(status_code=409, detail="标签名称已存在")
    for item_id in payload.item_ids:
        if item_id not in store.items:
            raise HTTPException(status_code=422, detail=f"衣物不存在：{item_id}")


def list_labels() -> list[Label]:
    """列出标签，并标明之后已被删除的衣物引用。"""
    return [_render(label) for label in labels.values()]


def get_label(label_id: UUID) -> Label:
    label = labels.get(label_id)
    if label is None:
        raise HTTPException(status_code=404, detail="标签不存在")
    return _render(label)


def create_label(payload: LabelInput) -> Label:
    """保存名称唯一且引用有效的标签。"""
    _check(payload)
    label = Label(**payload.model_dump())
    labels[label.id] = label
    return _render(label)


def replace_label(label_id: UUID, payload: LabelInput) -> Label:
    get_label(label_id)
    _check(payload, exclude_id=label_id)
    label = Label(id=label_id, **payload.model_dump())
    labels[label_id] = label
    return _render(label)


def delete_label(label_id: UUID) -> None:
    get_label(label_id)
    del labels[label_id]
