# FastAPI 与 Naive RAG 学习项目

通过一个逐步完善的文档问答项目，学习 FastAPI、大模型调用、LangChain 和 Naive RAG。每次完成一个可验证的小任务，具体安排见 [第一周学习计划](第一周学习计划.md)。

## 当前进度

- 已有 `main.py`，包含 `GET /` 的 Hello World 示例。
- 环境已就绪：`pyproject.toml`、`uv.lock` 已生成，`.venv` 使用 uv 管理的 CPython 3.12.13，已安装 `fastapi[standard]`。
- 当前学习进度：第 1 天第一关已通过，下一步是第二关，学习路径参数与查询参数。
- 助手已通过 `curl` 和浏览器 `/docs` 验证 `GET /` 返回状态码 `200` 和 `{"Hello":"World"}`；学习者已说明应用对象、路由装饰器和处理函数的基本关系，验收记录见学习计划。
- 模型调用、文档检索、问答接口和 Docker 部署将在后续步骤中逐步实现。

任务勾选和学习记录统一维护在 [第一周学习计划](第一周学习计划.md) 中。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [main.py](main.py) | FastAPI 应用入口，目前包含 Hello World 路由 |
| [第一周学习计划.md](第一周学习计划.md) | 每日任务、验收标准、进度勾选和复盘记录 |
| [AGENTS.md](AGENTS.md) | AI 助手在本项目中的协作与开发约定 |
| [README.md](README.md) | 项目介绍、运行方法和学习入口 |

## 运行 Hello World

本项目约定使用 Python 3.12 和 `uv` 管理环境与依赖。以下命令在项目根目录执行。

### 首次准备环境

项目名使用 `fastapi-rag-learning`，避免与依赖包 `fastapi` 同名（同名时 `uv add` 会报 self-dependency 错误）。

初始化命令如下，**已执行过，无需重复**：

```bash
uv init --bare --python 3.12
uv add "fastapi[standard]"
```

完成后会生成 `pyproject.toml`、`uv.lock` 与 `.venv`。

> 踩坑记录：如果 `.venv` 是别处或旧版解释器建的（例如 Homebrew Python 3.15 报 `platform.mac_ver()` 为空），`uv` 会继续复用它并报 `Broken Python installation`。此时删除重建即可：`rm -rf .venv && uv venv --python 3.12`。

### 启动服务

```bash
uv run fastapi dev main.py
```

保持终端运行，在浏览器访问：

```text
http://127.0.0.1:8000/
```

预期响应：

```json
{"Hello": "World"}
```

交互式接口文档地址：

```text
http://127.0.0.1:8000/docs
```

展开 `GET /`，点击 `Try it out` → `Execute`，检查响应状态码是否为 `200`。

也可以在另一个终端检查接口：

```bash
curl http://127.0.0.1:8000/
```

停止服务时，在运行服务的终端按 `Ctrl+C`。

### 已有依赖配置时恢复环境

完成首次初始化、已有 `pyproject.toml` 和 `uv.lock` 后，可以使用：

```bash
uv sync
uv run fastapi dev main.py
```

## 本周目标

最终实现一个接收问题的 `POST /ask` 接口，根据本地 Markdown/TXT 文档生成答案，并返回检索到的参考片段与来源。

计划使用 FastAPI、Pydantic、LangChain 和 FAISS，最后通过 Docker 在本地运行。具体依赖在对应学习步骤中引入。

```text
建库：文档 → 加载 → 分块 → Embedding → FAISS 索引
问答：问题 → 检索相关片段 → 提示词 → 模型 → 答案与参考片段
```

## 学习节奏

每次安排 60–90 分钟，做不完就顺延。先理解当前小步骤的目标，再实现和验证；完成验收后继续下一项。

下一步从 [第 1 天第二关：接收请求参数](第一周学习计划.md#第二关接收请求参数) 开始。
