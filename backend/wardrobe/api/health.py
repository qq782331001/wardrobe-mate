"""服务状态接口。"""

from fastapi import APIRouter


router = APIRouter(tags=["服务状态"])


@router.get("/health")
async def health() -> dict[str, str]:
    """返回服务状态。"""
    return {"status": "ok"}
