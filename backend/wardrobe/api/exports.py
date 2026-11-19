"""衣橱数据导出接口。"""

from fastapi import APIRouter

from wardrobe.models.export import WardrobeExport
from wardrobe.services import exports as export_service


router = APIRouter(prefix="/export", tags=["数据导出"])


@router.get("")
async def export_wardrobe() -> WardrobeExport:
    """导出当前进程中的衣物、搭配和穿着记录。"""
    return export_service.export_wardrobe()
