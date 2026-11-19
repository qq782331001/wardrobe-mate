# 后端代码

基于 Python 3.11+、FastAPI 和 Pydantic 的本地原型。仍使用进程内存保存数据，没有接入数据库或外部服务。

## 目录

```text
backend/
  main.py              应用入口与路由组装
  requirements.txt     Python 依赖
  wardrobe/
    api/               HTTP 接口
    models/            请求与返回模型
    services/          衣物、搭配、记录和推荐逻辑
    storage/           单进程内存存储
```

路由负责接收请求与返回结果，模型负责约束输入，业务模块处理内存数据。当前接口在单个异步调用内完成同步内存操作；加入外部 I/O、线程或持久化时需要重新考虑并发与事务边界。

## 启动

在仓库根目录使用 PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

接口文档地址：`http://127.0.0.1:8000/docs`。启动命令保留单进程模式，不要为当前内存原型增加多个 worker。

## 模块入口

| 路径 | 内容 |
| --- | --- |
| `/health` | 服务健康状态 |
| `/items` | 衣物增删改查与分类、可用状态筛选 |
| `/outfits` | 搭配增删改查与单品引用检查 |
| `/wear-logs` | 穿着记录增删改查与日期筛选 |
| `/recommendations` | 从已保存搭配中按场景、锁定单品和穿着次数筛选 |
| `/statistics` | 衣物数量、分类分布与穿着次数统计 |
| `/catalog/categories` | 衣物分类值与中文名称 |
| `/export` | 导出当前进程内的衣物、搭配和记录 |

## 当前语义

- `PUT` 完整替换资源的可编辑字段，标识不变。
- 被搭配引用的衣物不能直接删除；被穿着记录引用的搭配也不能直接删除。
- 创建或修改穿着记录时，搭配内的衣物必须当前可用。
- 穿着记录引用现有搭配，不保存历史快照；修改搭配会影响历史统计，后续需要补充快照能力。
- 推荐只筛选已保存搭配，不自动生成新组合，不调用 AI，也不考虑实时天气。
- 统计来自当前保存的数据，不代表经过校验的长期历史。
- 导出内容是数据快照，目前没有对应的恢复或导入接口。

## 限制

重启会清空数据，多进程之间不共享。尚未提供账号隔离、持久化、文件上传、天气或 AI 接入，当前代码面向本地原型开发。

手动请求示例见 [requests](../requests/README.md)。
