"""当前进程保存的画布布局。"""

from uuid import UUID

from wardrobe.features.canvas.models import CanvasInput


# ponytail: 仅保存布局元数据，重启丢失；生产使用前需持久化并按用户隔离。
canvases: dict[UUID, CanvasInput] = {}
