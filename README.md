# FastAPI 与 Naive RAG 学习项目

通过一个逐步完善的文档问答项目，学习 FastAPI、大模型调用、LangChain 和 Naive RAG。每次完成一个可验证的小任务，具体安排见 [第一周学习计划](第一周学习计划.md)。

## 当前进度

- 已有 `main.py`，包含 `GET /` 的 Hello World 示例、支持路径参数和可选查询参数的 `GET /hello/{name}` 问候接口，以及接收并返回 JSON 问题的 `POST /questions` 接口。
- 环境已就绪：`pyproject.toml`、`uv.lock` 已生成，`.venv` 使用 uv 管理的 CPython 3.12.13，已安装 `fastapi[standard]`、`langchain-openai` 和 `langchain-text-splitters`。
- 当前学习进度：第 1 天和第 2 天均已完成验收。已完成模型服务选择、`.env` 配置、首次模型调用、提示词模板、字符串输出解析器和 LCEL；同一条 Chain 的 `Pydantic`、`FastAPI` 两种主题均得到对应的三句话解释和 `True`，各组件职责及输出传递的基础理解已验收。第 3 天五项操作任务均已完成，包含块大小从 300 调整为 500 后的内容比较；代码与运行已有验证依据，块大小、重叠和内容相关性的整体概念理解继续巩固。
- 助手已通过 `curl` 和浏览器 `/docs` 验证 `GET /` 返回状态码 `200` 和 `{"Hello":"World"}`；学习者已说明应用对象、路由装饰器和处理函数的基本关系，验收记录见学习计划。
- 已有独立的 `llm_demo.py` 模型调用示例；文档检索、问答接口和 Docker 部署将在后续步骤中逐步实现。

任务勾选和学习记录统一维护在 [第一周学习计划](第一周学习计划.md) 中。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [main.py](main.py) | FastAPI 应用入口，包含 Hello World、问候路由和接收 JSON 问题的接口 |
| [llm_demo.py](llm_demo.py) | 独立的 LCEL 示例，读取配置，通过模板、模型、解析器组成的 Chain 解释 `topic` 并打印字符串结果 |
| [data/notes.md](data/notes.md) | 第 3 天的 RAG 练习材料，记录当前项目中的路由、参数、请求体与校验 |
| [load_demo.py](load_demo.py) | 读取练习文档，创建包含正文和来源元数据的 `Document`，打印正文、元数据及字符数 |
| [split_demo.py](split_demo.py) | 将练习文档分块，打印文本块数量，以及前 3 块的正文、字符数与来源 |
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

脚本使用 `ChatPromptTemplate` 定义“请用三句话解释什么是 {topic}。”，通过 `chain = prompt | llm | parser` 连接提示词模板、模型和 `StrOutputParser`。调用 `chain.invoke({"topic": "FastAPI"})` 后，依次填入主题、请求模型、将回复消息解析为正文字符串，最后打印正文及 `isinstance(result, str)` 的检查结果。当前 `topic` 为 `FastAPI`；修改 `chain.invoke(...)` 中的主题值后重新运行，即可复用同一条 Chain 解释其他概念。

学习者此前在逐步调用版本中提供了 `FastAPI` 和 `Pydantic` 两个主题的输出，并说明模板填充与模型请求的区别，提示词模板验收通过。加入解析器后，学习者提供了 Pydantic 的三句话解释和 `True`，并确认解析器只处理已有消息、不再次请求模型服务，解析器验收通过。LCEL 版本已由助手只读核对代码；学习者先后将同一条 Chain 的主题设为 `Pydantic` 和 `FastAPI`，两次均得到对应的三句话解释和 `True`，并已说明 `llm` 的输出交给 `parser`、组件通过统一接口组合，LCEL 基础理解及两主题复用均已验收，第 2 天完成。以上模型运行依据均为学习者提供的实际输出，助手未另行请求模型服务。

## 运行文档加载示例

在项目根目录执行：

```bash
uv run python load_demo.py
```

脚本根据自身所在目录定位 `data/notes.md`，使用 Python 标准库 `pathlib` 以 UTF-8 读取正文，再创建 LangChain 的 `Document` 对象：`page_content` 保存正文，`metadata` 字典中的 `source` 保存文件的绝对路径。

预期输出为完整笔记、包含 `source` 的元数据字典，以及字符数；当前文档为 1322 个字符，包含 Markdown 标记、空格和换行。助手已使用项目的 `langchain-core` 1.7.3 环境执行 `uv run --no-sync python load_demo.py`，确认上述结果。学习者已准确说明 `page_content` 保存正文，`metadata` 保存来源等元数据，并提供 `uv run python load_demo.py` 的完整输出，正文、来源路径和字符数均符合预期，文档加载这一步通过。

## 运行文档分块示例

在项目根目录执行：

```bash
uv run python split_demo.py
```

脚本重新读取练习文档并创建 `Document`，再使用 `RecursiveCharacterTextSplitter` 分块。当前参数为 `chunk_size=500`、`chunk_overlap=50`、`length_function=len`：按字符数计量块大小，目标重叠为 50 个字符。分割器优先沿段落、换行等位置切分，实际块长与重叠受切分位置影响。本次只把块大小从 300 调整为 500，用于比较内容边界。

`split_documents([document])` 接收文档列表，返回文本块的 `Document` 列表，并将原文档的元数据保留在块中。脚本打印总块数及前 3 块的正文、字符数和来源，便于观察分块边界。

在 `langchain-text-splitters` 1.1.3 环境中，同一份 1322 个字符的笔记有如下结果：

| 块大小 | 目标重叠 | 总块数 | 前 3 块字符数 | 验证依据 |
| --- | --- | --- | --- | --- |
| 300 | 50 | 6 | 182、279、293 | 助手运行与学习者实际输出 |
| 500（当前） | 50 | 3 | 463、466、388 | 助手运行；学习者已提供第一块的正文、长度及来源 |

当前三块的来源均指向原笔记。原先第一块只包含根路由的说明，调整后第一块还包含问候路由和路径参数的说明；参数调整与两组内容边界的比较已完成。学习者已理解块大小上限，并识别只看到结论时可能缺少条件；块太大、太小、重叠影响及内容相关性的整体概念理解继续巩固，与操作任务完成状态单独记录。

## 本周目标

最终实现一个接收问题的 `POST /ask` 接口，根据本地 Markdown/TXT 文档生成答案，并返回检索到的参考片段与来源。

计划使用 FastAPI、Pydantic、LangChain 和 FAISS，最后通过 Docker 在本地运行。具体依赖在对应学习步骤中引入。

```text
建库：文档 → 加载 → 分块 → Embedding → FAISS 索引
问答：问题 → 检索相关片段 → 提示词 → 模型 → 答案与参考片段
```

## 学习节奏

每次安排 60–90 分钟，做不完就顺延。先理解当前小步骤的目标，再实现和验证；完成验收后继续下一项。

第 1 天和第 2 天均已完成验收。第 3 天五项操作任务均已完成：参数已从 300 调整为 500，助手运行验证完成，学习者已提供新第一块的正文、463 个字符的长度及正确来源，两组内容边界已完成对照。接下来巩固块大小、重叠和内容相关性的概念；整体概念验收与操作任务完成状态单独记录。任务勾选和验收依据见 [第一周学习计划](第一周学习计划.md)。
