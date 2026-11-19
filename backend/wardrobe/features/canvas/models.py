"""画布尺寸、衣物图层与动态引用状态。"""

from uuid import UUID

from pydantic import Field, field_validator

from wardrobe.models.base import InputModel


class CanvasLayer(InputModel):
    """一件真实衣物在画布中的变换信息。"""

    item_id: UUID
    x: float = Field(default=0, allow_inf_nan=False)
    y: float = Field(default=0, allow_inf_nan=False)
    scale: float = Field(default=1, ge=0.05, le=20, allow_inf_nan=False)
    rotation: float = Field(default=0, allow_inf_nan=False)
    opacity: float = Field(default=1, ge=0, le=1, allow_inf_nan=False)
    z_index: int = Field(default=0, ge=-100, le=100)


class CanvasInput(InputModel):
    """完整替换一套搭配的布局，允许空画布。"""

    width: int = Field(ge=100, le=8192)
    height: int = Field(ge=100, le=8192)
    layers: list[CanvasLayer] = Field(default_factory=list, max_length=30)

    @field_validator("layers")
    @classmethod
    def reject_duplicate_layers(cls, values: list[CanvasLayer]) -> list[CanvasLayer]:
        """同一件衣物最多对应一个图层。"""
        ids = [layer.item_id for layer in values]
        if len(ids) != len(set(ids)):
            raise ValueError("画布不能重复引用同一件衣物")
        return values


class CanvasDocument(CanvasInput):
    """返回保存的布局，以及当前衣橱中的引用状态。"""

    outfit_id: UUID
    outfit_exists: bool
    missing_item_ids: list[UUID]
    unavailable_item_ids: list[UUID]
