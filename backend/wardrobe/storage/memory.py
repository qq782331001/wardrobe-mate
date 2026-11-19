"""为同一进程中的业务模块共享衣橱数据。"""

from dataclasses import dataclass, field
from uuid import UUID

from wardrobe.models.item import Item
from wardrobe.models.outfit import Outfit
from wardrobe.models.wear_log import WearLog


@dataclass
class MemoryStore:
    """集中保存衣物、搭配与穿着记录。"""

    items: dict[UUID, Item] = field(default_factory=dict)
    outfits: dict[UUID, Outfit] = field(default_factory=dict)
    wear_logs: dict[UUID, WearLog] = field(default_factory=dict)


# ponytail: 重启丢失数据，多进程不共享；生产使用前需持久化并按用户隔离。
store = MemoryStore()
