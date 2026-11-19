"""数字衣橱起步版：提供衣物与搭配的内存管理接口。"""

from enum import Enum
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class Category(str, Enum):
    """衣物所属部位，用于衣橱分类和筛选。"""

    TOP = "TOP"
    BOTTOM = "BOTTOM"
    OUTER = "OUTER"
    ONE_PIECE = "ONE_PIECE"
    SHOES = "SHOES"
    ACC = "ACC"


class InputModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class ItemInput(InputModel):
    name: str = Field(min_length=1, max_length=120)
    category: Category
    color: str | None = Field(default=None, max_length=40)
    image_url: HttpUrl | None = None
    available: bool = True


class Item(ItemInput):
    id: UUID = Field(default_factory=uuid4)


class OutfitInput(InputModel):
    name: str = Field(min_length=1, max_length=120)
    item_ids: list[UUID] = Field(min_length=1, max_length=30)
    occasion: str | None = Field(default=None, max_length=80)

    @field_validator("item_ids")
    @classmethod
    def reject_duplicate_items(cls, item_ids: list[UUID]) -> list[UUID]:
        if len(item_ids) != len(set(item_ids)):
            raise ValueError("同一套搭配不能重复引用单品")
        return item_ids


class Outfit(OutfitInput):
    id: UUID = Field(default_factory=uuid4)


app = FastAPI(
    title="Wardrobe Mate",
    version="0.1.0",
    description="数字衣橱起步版，数据仅保存在当前进程内。",
)

# ponytail: 重启会丢失数据，多进程间不共享；生产使用前需持久化并按用户隔离。
items: dict[UUID, Item] = {}
outfits: dict[UUID, Outfit] = {}


def require_item(item_id: UUID) -> Item:
    """获取指定衣物，不存在时返回明确的资源错误。"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="衣物不存在")
    return items[item_id]


def require_outfit(outfit_id: UUID) -> Outfit:
    """获取指定搭配，不存在时返回明确的资源错误。"""
    if outfit_id not in outfits:
        raise HTTPException(status_code=404, detail="搭配不存在")
    return outfits[outfit_id]


def check_outfit_items(item_ids: list[UUID]) -> None:
    """保存搭配前确认引用的单品真实存在且当前可用。"""
    for item_id in item_ids:
        item = items.get(item_id)
        if item is None:
            raise HTTPException(status_code=422, detail=f"衣物不存在：{item_id}")
        if not item.available:
            raise HTTPException(status_code=422, detail=f"衣物当前不可用：{item_id}")


@app.get("/health")
async def health() -> dict[str, str]:
    """返回服务状态。"""
    return {"status": "ok"}


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemInput) -> Item:
    """新增衣物，图片地址仅作为引用保存，不发起下载请求。"""
    item = Item(**payload.model_dump())
    items[item.id] = item
    return item


@app.get("/items")
async def list_items(
    category: Category | None = None,
    available: bool | None = None,
) -> list[Item]:
    """列出衣物，可按分类和当前可用状态筛选。"""
    return [
        item
        for item in items.values()
        if (category is None or item.category == category)
        and (available is None or item.available == available)
    ]


@app.get("/items/{item_id}")
async def get_item(item_id: UUID) -> Item:
    """查看指定衣物。"""
    return require_item(item_id)


@app.put("/items/{item_id}")
async def replace_item(item_id: UUID, payload: ItemInput) -> Item:
    """完整更新衣物信息，保留原单品标识。"""
    require_item(item_id)
    item = Item(id=item_id, **payload.model_dump())
    items[item_id] = item
    return item


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID) -> Response:
    """删除未被搭配引用的衣物，防止留下失效的单品引用。"""
    require_item(item_id)
    if any(item_id in outfit.item_ids for outfit in outfits.values()):
        raise HTTPException(status_code=409, detail="衣物仍被搭配引用，请先修改或删除相关搭配")
    del items[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/outfits", status_code=status.HTTP_201_CREATED)
async def create_outfit(payload: OutfitInput) -> Outfit:
    """使用衣橱内可用的真实单品保存一套搭配。"""
    check_outfit_items(payload.item_ids)
    outfit = Outfit(**payload.model_dump())
    outfits[outfit.id] = outfit
    return outfit


@app.get("/outfits")
async def list_outfits() -> list[Outfit]:
    """列出已保存的搭配，包括单品后来变为不可用的历史搭配。"""
    return list(outfits.values())


@app.get("/outfits/{outfit_id}")
async def get_outfit(outfit_id: UUID) -> Outfit:
    """查看指定搭配。"""
    return require_outfit(outfit_id)


@app.put("/outfits/{outfit_id}")
async def replace_outfit(outfit_id: UUID, payload: OutfitInput) -> Outfit:
    """完整更新搭配，并重新检查所有单品的可用状态。"""
    require_outfit(outfit_id)
    check_outfit_items(payload.item_ids)
    outfit = Outfit(id=outfit_id, **payload.model_dump())
    outfits[outfit_id] = outfit
    return outfit


@app.delete("/outfits/{outfit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_outfit(outfit_id: UUID) -> Response:
    """删除搭配，保留其引用的衣物。"""
    require_outfit(outfit_id)
    del outfits[outfit_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
