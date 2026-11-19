"""统一处理输入字段和字符串空白。"""

from pydantic import BaseModel, ConfigDict


class InputModel(BaseModel):
    """拒绝未定义字段，去除输入字符串两端的空白。"""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
