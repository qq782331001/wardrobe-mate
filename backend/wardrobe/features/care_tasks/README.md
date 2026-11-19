# 衣物护理任务

记录洗涤、干洗或修补安排，数据仅保存在当前进程内。

| 方法与路径 | 用途 |
| --- | --- |
| `POST /care-tasks` | 新增任务 |
| `GET /care-tasks?status=pending` | 按状态查看列表 |
| `GET /care-tasks/{id}` | 查看任务 |
| `PUT /care-tasks/{id}` | 完整更新任务 |
| `DELETE /care-tasks/{id}` | 删除任务 |

`kind` 可为 `wash`、`dry_clean`、`repair`；状态为 `pending` 或 `done`。
创建和更新时必须引用存在的衣物。衣物之后被删除，任务仍会保留，返回的 `item_exists` 为 `false`。
任务完成不会自动修改衣物的 `available`，需要通过衣物接口单独维护。
重启清空任务，多进程不共享，尚无账号隔离或自动提醒。
