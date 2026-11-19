# 衣物集合

把衣物整理成通勤、换季等主题集合。集合名称允许重复，也允许先创建空集合。

| 接口 | 用途 |
| --- | --- |
| `GET /collections` | 集合列表 |
| `POST /collections` | 创建集合 |
| `GET /collections/{id}` | 集合详情 |
| `PUT /collections/{id}` | 完整更新集合 |
| `DELETE /collections/{id}` | 删除集合，保留衣物 |

支持名称、描述及最多 200 个不重复单品 ID。创建和修改时，所有引用衣物必须存在。

核心衣物后来被删除时，集合不自动删除引用，读取结果通过 `missing_item_ids` 标明缺失单品。

数据仅在当前进程内保存，重启丢失，无账号隔离。示例见 `requests/collections.http`。
