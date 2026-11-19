"""衣物集合的单进程内存状态。"""

from uuid import UUID

from wardrobe.features.collections.models import Collection


collections: dict[UUID, Collection] = {}
