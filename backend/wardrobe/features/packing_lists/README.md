# 出行行李清单

保存出行日期、目的地、携带衣物和装箱进度，数据仅在当前进程内保留。

| 方法与路径 | 用途 |
| --- | --- |
| `POST /packing-lists` | 新增清单 |
| `GET /packing-lists` | 查看所有清单 |
| `GET /packing-lists/{id}` | 查看指定清单 |
| `PUT /packing-lists/{id}` | 完整更新清单与装箱状态 |
| `DELETE /packing-lists/{id}` | 删除清单 |

`packed_item_ids` 必须是 `item_ids` 的子集，两者都不允许重复。
清单允许包含当前不可用的真实衣物，读取时通过 `unavailable_item_ids` 标识。
衣物后来被删除时保留清单，并通过 `missing_item_ids` 标识；重新保存时需移除无效引用。
清单不会修改衣物可用状态，不检查出行目的地天气，也不自动推荐携带数量。
重启清空数据，多进程不共享，尚无账号隔离。
