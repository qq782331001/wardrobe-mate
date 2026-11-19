"""统一搜索关键字和字段的大小写与空白处理。"""


def normalize_query(value: str) -> str:
    """去除两端空白并折叠大小写，不进行分词或语义推断。"""
    return value.strip().casefold()


def contains_query(query: str, *values: str | None) -> bool:
    """判断至少一个实际字段包含已经标准化的非空关键字。"""
    return bool(query) and any(
        query in normalize_query(value)
        for value in values
        if value is not None
    )
