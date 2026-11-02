# FastAPI 与 Naive RAG 学习项目

通过一个逐步完善的文档问答项目，学习 FastAPI、大模型调用、LangChain 和 Naive RAG。每次完成一个可验证的小任务，具体安排见 [第一周学习计划](第一周学习计划.md)。

## 当前进度

- 已有 `main.py`，包含 `GET /` 的 Hello World 示例与支持路径参数、可选查询参数的 `GET /hello/{name}` 问候接口。
- 环境已就绪：`pyproject.toml`、`uv.lock` 已生成，`.venv` 使用 uv 管理的 CPython 3.12.13，已安装 `fastapi[standard]`。
- 当前学习进度：第 1 天第一关和第二关均已通过；路径参数与可选查询参数的实现、运行及基础概念均已验收，下一步是第三关，接收并校验 JSON 请求体。
- 助手已通过 `curl` 和浏览器 `/docs` 验证 `GET /` 返回状态码 `200` 和 `{"Hello":"World"}`；学习者已说明应用对象、路由装饰器和处理函数的基本关系，验收记录见学习计划。
- 模型调用、文档检索、问答接口和 Docker 部署将在后续步骤中逐步实现。

任务勾选和学习记录统一维护在 [第一周学习计划](第一周学习计划.md) 中。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [main.py](main.py) | FastAPI 应用入口，包含 Hello World 与可选择中英文的问候路由 |
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

### 验证路径参数与查询参数

服务运行时，可在另一个终端执行：

```bash
curl -sS -i http://127.0.0.1:8000/hello/xuzhi
curl -sS -i 'http://127.0.0.1:8000/hello/xuzhi?language=en'
curl -sS -i 'http://127.0.0.1:8000/hello/xuzhi?language=zh'
```

以上三次请求已由助手验证，均返回状态码 `200`。不传 `language` 或传入 `en`，响应体均为 `{"message":"Hello, xuzhi!"}`；传入 `zh` 时为 `{"message":"你好，xuzhi！"}`。

当前 `language` 的默认值是 `"en"`，只有值为 `"en"` 时返回英文，其余字符串都返回中文；目前未限制语言取值。

也可在 `/docs` 中展开 `GET /hello/{name}`，点击 `Try it out`，填写 `name` 和 `language` 后点击 `Execute`，对比 `en` 与 `zh` 的结果。学习者已反馈完成此操作；助手随后在浏览器中分别执行两次请求，确认实际状态码均为 `200`，响应体分别为 `{"message":"Hello, xuzhi!"}` 和 `{"message":"你好，xuzhi！"}`。截图见 [英文响应](output/playwright/docs-hello-en-response.png) 和 [中文响应](output/playwright/docs-hello-zh-response.png)。

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

第 1 天第二关已通过。下一步从 [第三关：接收并校验 JSON](第一周学习计划.md#第三关接收并校验-json) 开始，先学习用 Pydantic 定义包含 `question` 字段的请求模型。
