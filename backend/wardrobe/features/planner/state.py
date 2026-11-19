"""穿搭计划的进程内状态。"""

from uuid import UUID

from wardrobe.features.planner.models import Plan


# ponytail: 重启清空且多进程不共享，持久化时替换此存储。
plans: dict[UUID, Plan] = {}
