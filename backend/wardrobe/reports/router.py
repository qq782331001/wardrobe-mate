"""CSV 下载接口。"""

from fastapi import APIRouter, Response

from wardrobe.reports.items import download_items
from wardrobe.reports.outfits import download_outfits
from wardrobe.reports.wear_logs import download_wear_logs


router = APIRouter(prefix="/reports", tags=["表格导出"])


@router.get("/items.csv", response_class=Response)
async def items_csv() -> Response:
    """下载衣物明细表。"""
    return download_items()


@router.get("/outfits.csv", response_class=Response)
async def outfits_csv() -> Response:
    """下载搭配明细表。"""
    return download_outfits()


@router.get("/wear-logs.csv", response_class=Response)
async def wear_logs_csv() -> Response:
    """下载穿着记录表。"""
    return download_wear_logs()
