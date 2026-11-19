"""衣物标签接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.features.labels import service
from wardrobe.features.labels.models import Label, LabelInput


router = APIRouter(prefix="/labels", tags=["标签"])


@router.get("")
async def list_labels() -> list[Label]:
    return service.list_labels()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_label(payload: LabelInput) -> Label:
    return service.create_label(payload)


@router.get("/{label_id}")
async def get_label(label_id: UUID) -> Label:
    return service.get_label(label_id)


@router.put("/{label_id}")
async def replace_label(label_id: UUID, payload: LabelInput) -> Label:
    return service.replace_label(label_id, payload)


@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(label_id: UUID) -> Response:
    service.delete_label(label_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
