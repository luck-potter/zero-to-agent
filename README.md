# FastAPI 与 Naive RAG 学习项目

通过一个逐步完善的文档问答项目，学习 FastAPI、大模型调用、LangChain 和 Naive RAG。每次完成一个可验证的小任务，具体安排见 [第一周学习计划](第一周学习计划.md)。

## 当前进度

- 已有 `main.py`，包含 `GET /` 的 Hello World 示例、支持路径参数和可选查询参数的 `GET /hello/{name}` 问候接口，以及接收并返回 JSON 问题的 `POST /questions` 接口。
- 环境已就绪：`pyproject.toml`、`uv.lock` 已生成，`.venv` 使用 uv 管理的 CPython 3.12.13，已安装 `fastapi[standard]` 和 `langchain-openai`。
- 当前学习进度：第 1 天三关均已通过。第 2 天已完成模型服务选择、`.env` 配置与首次模型调用；学习者已提供成功的终端输出，并说明创建客户端与发送请求的区别。下一步是使用提示词模板接收 `topic`，当前待实现与验收。
- 助手已通过 `curl` 和浏览器 `/docs` 验证 `GET /` 返回状态码 `200` 和 `{"Hello":"World"}`；学习者已说明应用对象、路由装饰器和处理函数的基本关系，验收记录见学习计划。
- 已有独立的 `llm_demo.py` 模型调用示例；文档检索、问答接口和 Docker 部署将在后续步骤中逐步实现。

任务勾选和学习记录统一维护在 [第一周学习计划](第一周学习计划.md) 中。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [main.py](main.py) | FastAPI 应用入口，包含 Hello World、问候路由和接收 JSON 问题的接口 |
| [llm_demo.py](llm_demo.py) | 独立的模型调用示例，读取配置、发送固定问题并打印回答 |
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

### 提交 JSON 问题

服务运行时，可执行下面的命令：

```bash
curl -sS -i -X POST http://127.0.0.1:8000/questions \
  -H 'Content-Type: application/json' \
  -d '{"question":"什么是 FastAPI？","language":"zh"}'
```

预期状态码为 `200`，响应体为：

```json
{"question":"什么是 FastAPI？","language":"zh"}
```

接口目前原样返回问题与语言。`language` 可以省略，默认值为 `"en"`；`question` 必须是至少包含 1 个字符的字符串，缺少字段或提交空字符串 `""` 都会返回 `422`。

以上行为已由助手使用当前应用的本地 `TestClient` 验证。学习者已反馈完成 `/docs` 操作；助手随后使用 Playwright 在浏览器中展开 `POST /questions`，点击 `Try it out`，分别填写正常问题、`{}` 和 `{"question":""}` 并点击 `Execute`，确认 `Server response` 的实际状态码依次为 `200`、`422`、`422`，两次错误分别为 `missing` 和 `string_too_short`，均指向 `body → question`。三次响应头均包含 `content-type: application/json`，操作验收通过。截图见 [正常问题](output/playwright/docs-questions-valid-response.png)、[缺少字段](output/playwright/docs-questions-missing-response.png) 和 [空字符串](output/playwright/docs-questions-empty-response.png)。

### 已有依赖配置时恢复环境

完成首次初始化、已有 `pyproject.toml` 和 `uv.lock` 后，可以使用：

```bash
uv sync
uv run fastapi dev main.py
```

## 运行模型调用示例

在项目根目录创建本地 `.env`，将下面的占位符替换为实际配置：

```dotenv
OPENAI_BASE_URL=你的模型服务基地址
OPENAI_API_KEY=你的模型服务密钥
LLM_MODEL=gpt-6-luna
```

当前使用公司配置的 sub2api 网关，地址按公司提供的配置填写。本地 `.env` 已被 `.gitignore` 忽略，真实密钥不写入代码或文档。

在项目根目录执行：

```bash
uv run --env-file .env python llm_demo.py
```

脚本会发送“请用三句话解释什么是 FastAPI。”并打印模型回复。学习者已执行此命令并提供成功的终端输出，客户端创建与模型调用的基础概念已验收。提示词模板、输出解析器和 LCEL 尚未实现。

## 本周目标

最终实现一个接收问题的 `POST /ask` 接口，根据本地 Markdown/TXT 文档生成答案，并返回检索到的参考片段与来源。

计划使用 FastAPI、Pydantic、LangChain 和 FAISS，最后通过 Docker 在本地运行。具体依赖在对应学习步骤中引入。

```text
建库：文档 → 加载 → 分块 → Embedding → FAISS 索引
问答：问题 → 检索相关片段 → 提示词 → 模型 → 答案与参考片段
```

## 学习节奏

每次安排 60–90 分钟，做不完就顺延。先理解当前小步骤的目标，再实现和验证；完成验收后继续下一项。

第 1 天三关均已通过，第 2 天的模型配置和首次调用已完成验收。下一小步是使用提示词模板接收 `topic`，观察更换主题后的模型回复；任务勾选和验收依据见 [第一周学习计划](第一周学习计划.md)。
