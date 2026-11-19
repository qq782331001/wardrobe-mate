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
