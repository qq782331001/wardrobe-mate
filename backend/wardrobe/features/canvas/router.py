"""搭配画布布局的读取和保存接口。"""

from uuid import UUID

from fastapi import APIRouter, Response, status

from wardrobe.features.canvas import service
from wardrobe.features.canvas.models import CanvasDocument, CanvasInput


router = APIRouter(prefix="/canvas", tags=["画布布局"])


@router.get("/{outfit_id}")
async def get_canvas(outfit_id: UUID) -> CanvasDocument:
    """读取布局及当前引用状态。"""
    return service.get_canvas(outfit_id)


@router.put("/{outfit_id}")
async def replace_canvas(outfit_id: UUID, payload: CanvasInput) -> CanvasDocument:
    """创建或完整替换布局元数据，不渲染图片。"""
    return service.replace_canvas(outfit_id, payload)


@router.delete("/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_canvas(outfit_id: UUID) -> Response:
    """删除布局并保留核心搭配。"""
    service.delete_canvas(outfit_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
