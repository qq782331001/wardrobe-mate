"""提供与衣物分类枚举一致的显示选项。"""

from wardrobe.models.catalog import CategoryOption
from wardrobe.models.category import Category


def list_categories() -> list[CategoryOption]:
    """列出衣橱支持的分类及中文名称。"""
    labels = {
        Category.TOP: "上装",
        Category.BOTTOM: "下装",
        Category.OUTER: "外套",
        Category.ONE_PIECE: "连身",
        Category.SHOES: "鞋履",
        Category.ACC: "配饰",
    }
    return [CategoryOption(value=category, label=labels[category]) for category in Category]
