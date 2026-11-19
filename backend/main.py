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
from wardrobe.features.care_tasks.router import router as care_tasks_router
from wardrobe.features.collections.router import router as collections_router
from wardrobe.features.favorites.router import router as favorites_router
from wardrobe.features.labels.router import router as labels_router
from wardrobe.features.notes.router import router as notes_router
from wardrobe.features.packing_lists.router import router as packing_lists_router
from wardrobe.features.planner.router import router as planner_router
from wardrobe.features.wishlist.router import router as wishlist_router
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
    labels_router,
    collections_router,
    favorites_router,
    notes_router,
    care_tasks_router,
    packing_lists_router,
    planner_router,
    wishlist_router,
):
    app.include_router(router)
