"""标签仅保存于当前进程，不与其他进程共享。"""

from uuid import UUID

from wardrobe.features.labels.models import Label


labels: dict[UUID, Label] = {}
