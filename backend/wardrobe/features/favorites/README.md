# 收藏

收藏衣橱单品或已经保存的搭配。目标类型为 `item` 或 `outfit`。

| 接口 | 用途 |
| --- | --- |
| `GET /favorites` | 查询全部收藏，可按 `target_type` 筛选 |
| `POST /favorites` | 创建收藏 |
| `GET /favorites/{id}` | 查看收藏 |
| `DELETE /favorites/{id}` | 取消收藏 |

创建时要求目标存在；同一类型和 ID 的目标不能重复收藏，重复时返回 409。

核心衣物或搭配后来被删除时，收藏记录仍保留，读取结果的 `target_exists` 为 `false`。

收藏不会修改核心衣物和搭配，也不会影响推荐排序。数据仅存当前进程，重启丢失，无账号隔离。

手动请求示例见 `requests/favorites.http`。
