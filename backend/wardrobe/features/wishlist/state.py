"""愿望清单的进程内状态。"""

from uuid import UUID

from wardrobe.features.wishlist.models import Wish


# ponytail: 重启清空且多进程不共享，持久化时替换此存储。
wishes: dict[UUID, Wish] = {}
