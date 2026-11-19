# 待购愿望清单

记录尚未拥有的衣物，不自动加入 `/items`，也不会参与现有衣橱推荐。

| 方法与路径 | 用途 |
| --- | --- |
| `POST /wishlist` | 新增待购意向 |
| `GET /wishlist?priority=high` | 按分类与优先级筛选 |
| `GET /wishlist/{id}` | 查看待购意向 |
| `PUT /wishlist/{id}` | 完整更新待购意向 |
| `DELETE /wishlist/{id}` | 删除待购意向 |

`priority` 可为 `low`、`normal`、`high`。预算必须非负，最多两位小数，不进行币种换算。
`product_url` 仅保存 HTTP/HTTPS 地址，不抓取价格、库存或商品信息。
购买后需要通过衣物接口另行录入，不会自动完成支付或购买动作。
数据只在当前进程内保留，重启清空，多进程不共享，尚无账号隔离。
