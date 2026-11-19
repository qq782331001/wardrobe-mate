"""衣橱分类定义。"""

from enum import Enum


class Category(str, Enum):
    """按衣物所属部位分类，供录入与筛选共用。"""

    TOP = "TOP"
    BOTTOM = "BOTTOM"
    OUTER = "OUTER"
    ONE_PIECE = "ONE_PIECE"
    SHOES = "SHOES"
    ACC = "ACC"
