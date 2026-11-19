"""当前进程中衣橱数据的导出模型。"""

from pydantic import BaseModel

from wardrobe.models.item import Item
from wardrobe.models.outfit import Outfit
from wardrobe.models.wear_log import WearLog


class WardrobeExport(BaseModel):
    """汇总衣物、搭配与穿着记录，不代表持久化备份服务。"""

    items: list[Item]
    outfits: list[Outfit]
    wear_logs: list[WearLog]
