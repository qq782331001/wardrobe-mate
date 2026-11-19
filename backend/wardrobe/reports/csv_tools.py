"""共用 CSV 编码与下载响应。"""

import csv
from collections.abc import Iterable, Sequence
from io import StringIO

from fastapi import Response


def safe_cell(value: object) -> object:
    """将空值留空，避免用户文本被表格软件当作公式执行。"""
    if value is None:
        return ""
    if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value


def csv_download(
    filename: str,
    header: Sequence[str],
    rows: Iterable[Sequence[object]],
) -> Response:
    """生成带 UTF-8 标记的 CSV；文件名由内部接口固定指定。"""
    output = StringIO(newline="")
    writer = csv.writer(output)
    writer.writerow(header)
    for row in rows:
        writer.writerow([safe_cell(value) for value in row])
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
