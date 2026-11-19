"""衣物与搭配的文本搜索结果。"""

from wardrobe.models.base import InputModel
from wardrobe.models.item import Item
from wardrobe.models.outfit import Outfit


class SearchResult(InputModel):
    """总数为截取之前的匹配数量，列表分别受 limit 限制。"""

    items: list[Item]
    outfits: list[Outfit]
    item_total: int
    outfit_total: int
