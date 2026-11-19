"""收藏的单进程内存状态。"""

from uuid import UUID

from wardrobe.features.favorites.models import Favorite


favorites: dict[UUID, Favorite] = {}
