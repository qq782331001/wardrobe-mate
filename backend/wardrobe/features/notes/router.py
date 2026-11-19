"""衣物与搭配备注接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.features.notes import service
from wardrobe.features.notes.models import Note, NoteInput, TargetType


router = APIRouter(prefix="/notes", tags=["备注"])


@router.get("")
async def list_notes(target_type: TargetType | None = None, target_id: UUID | None = None) -> list[Note]:
    return service.list_notes(target_type, target_id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_note(payload: NoteInput) -> Note:
    return service.create_note(payload)


@router.get("/{note_id}")
async def get_note(note_id: UUID) -> Note:
    return service.get_note(note_id)


@router.put("/{note_id}")
async def replace_note(note_id: UUID, payload: NoteInput) -> Note:
    return service.replace_note(note_id, payload)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: UUID) -> Response:
    service.delete_note(note_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
