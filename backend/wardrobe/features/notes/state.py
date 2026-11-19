"""备注的单进程内存状态。"""

from uuid import UUID

from wardrobe.features.notes.models import Note


notes: dict[UUID, Note] = {}
