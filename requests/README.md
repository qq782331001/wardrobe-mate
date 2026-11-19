# 手动请求示例

这些 `.http` 文件用于手动调用接口，不是自动测试，不会随应用启动而执行。

先按 [后端说明](../backend/README.md) 启动本地服务，再使用支持 `.http` 格式的 HTTP 客户端打开对应文件。

## 建议顺序

1. `health.http`：查看服务状态。
2. `catalog.http`：获取分类字典。
3. `items.http`：新增衣物，复制响应中的真实 ID。
4. `outfits.http`：将衣物 ID 填入请求，新增搭配并复制搭配 ID。
5. `wear-logs.http`：使用真实搭配 ID 记录穿着。
6. `recommendations.http`：筛选已有搭配，按需锁定真实单品。
7. `statistics.http`：查看当前数据统计。
8. `export.http`：获取当前数据快照。

文件中的全零 UUID 只是占位值，需要替换。`PUT` 表示完整更新，示例请求不会自动串联。删除操作会修改当前内存数据，请逐条选择需要的请求。

重启开发服务后，旧 ID 会随内存数据清空而失效，需要重新创建衣物和搭配。

## 扩展示例

| 文件 | 内容 |
| --- | --- |
| `labels.http` | 标签和标签内单品 |
| `collections.http` | 衣物集合 |
| `favorites.http` | 收藏衣物或搭配 |
| `notes.http` | 资源备注 |
| `care-tasks.http` | 洗护维修安排 |
| `packing-lists.http` | 出行清单和已打包单品 |
| `planner.http` | 按日期安排搭配 |
| `wishlist.http` | 独立的待购清单 |
| `profile.http` | 本地演示偏好 |
| `canvas.http` | 保存与读取搭配布局 |
| `search.http` | 文本搜索 |
| `insights.http` | 指定日期窗口的穿着分析 |
| `reports.http` | CSV 明细下载 |

扩展示例需要各自填写真实的资源 ID。画布接口只处理布局 JSON，不生成穿搭图片；搜索与推荐均没有调用大模型。
