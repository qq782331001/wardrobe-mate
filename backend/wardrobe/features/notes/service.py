"""维护衣物与搭配备注，不自动删除历史记录。"""

from uuid import UUID

from fastapi import HTTPException

from wardrobe.features.notes.models import Note, NoteInput, TargetType
from wardrobe.features.notes.state import notes
from wardrobe.storage.memory import store


def _target_exists(target_type: TargetType, target_id: UUID) -> bool:
    return target_id in (store.items if target_type == "item" else store.outfits)


def _render(note: Note) -> Note:
    return note.model_copy(update={"target_exists": _target_exists(note.target_type, note.target_id)})


def _check(payload: NoteInput) -> None:
    if not _target_exists(payload.target_type, payload.target_id):
        raise HTTPException(status_code=422, detail="备注目标不存在")


def list_notes(target_type: TargetType | None = None, target_id: UUID | None = None) -> list[Note]:
    return [_render(note) for note in notes.values()
            if (target_type is None or note.target_type == target_type)
            and (target_id is None or note.target_id == target_id)]


def get_note(note_id: UUID) -> Note:
    note = notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="备注不存在")
    return _render(note)


def create_note(payload: NoteInput) -> Note:
    """为存在的衣物或搭配保存备注。"""
    _check(payload)
    note = Note(**payload.model_dump())
    notes[note.id] = note
    return _render(note)


def replace_note(note_id: UUID, payload: NoteInput) -> Note:
    get_note(note_id)
    _check(payload)
    note = Note(id=note_id, **payload.model_dump())
    notes[note_id] = note
    return _render(note)


def delete_note(note_id: UUID) -> None:
    get_note(note_id)
    del notes[note_id]
