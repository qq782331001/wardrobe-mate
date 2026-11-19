"""数字衣橱后端入口，组装各业务模块的接口。"""

from fastapi import FastAPI

from wardrobe.api import (
    catalog,
    exports,
    health,
    items,
    outfits,
    recommendations,
    statistics,
    wear_logs,
)
from wardrobe.reports.router import router as reports_router


app = FastAPI(
    title="Wardrobe Mate",
    version="0.3.0",
    description="数字衣橱本地原型，提供衣物、搭配和穿着记录等内存管理接口。",
)

for router in (
    health.router,
    items.router,
    outfits.router,
    wear_logs.router,
    recommendations.router,
    statistics.router,
    catalog.router,
    exports.router,
    reports_router,
):
    app.include_router(router)
