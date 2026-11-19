"""行李清单的本地进程状态。"""

from uuid import UUID

from wardrobe.features.packing_lists.models import PackingList


# ponytail: 重启清空且多进程不共享，持久化时替换此存储。
packing_lists: dict[UUID, PackingList] = {}
