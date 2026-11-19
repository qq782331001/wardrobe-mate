"""衣物分类目录接口。"""

from fastapi import APIRouter

from wardrobe.models.catalog import CategoryOption
from wardrobe.services import catalog as catalog_service


router = APIRouter(prefix="/catalog", tags=["分类目录"])


@router.get("/categories")
async def list_categories() -> list[CategoryOption]:
    """列出衣物分类及对应的中文名称。"""
    return catalog_service.list_categories()
