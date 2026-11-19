"""护理任务的进程内状态。"""

from uuid import UUID

from wardrobe.features.care_tasks.models import CareTask


# ponytail: 重启清空且多进程不共享，持久化时替换此存储。
tasks: dict[UUID, CareTask] = {}
