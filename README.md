# FastAPI 与 Naive RAG 学习项目

通过一个逐步完善的文档问答项目，学习 FastAPI、大模型调用、LangChain 和 Naive RAG。每次完成一个可验证的小任务，具体安排见 [第一周学习计划](第一周学习计划.md)。

## 当前进度

- 已有 `src/main.py`，包含 `GET /` 的 Hello World 示例、支持路径参数和可选查询参数的 `GET /hello/{name}` 问候接口，以及接收并返回 JSON 问题的 `POST /questions` 接口。
- 环境已就绪：`pyproject.toml`、`uv.lock` 已生成，`.venv` 使用 uv 管理的 CPython 3.12.13，已安装 `fastapi[standard]`、`langchain-openai`、`langchain-text-splitters`、`langchain-huggingface`、`sentence-transformers`、`faiss-cpu` 和 `numpy`。
- 当前学习进度：第 1–3 天均已完成基础验收。已完成模型服务选择、`.env` 配置、首次模型调用、提示词模板、字符串输出解析器和 LCEL；同一条 Chain 的 `Pydantic`、`FastAPI` 两种主题均得到对应的三句话解释和 `True`，各组件职责及输出传递的基础理解已验收。第 3 天文档加载、分块及块大小从 300 调整为 500 后的内容比较均已完成，块大小、重叠和内容相关性的基础概念已获得学习者确认。第 4 天单句与文本块向量化均已验收：助手与学习者的文本块向量化运行结果均为 3 个文本块各对应一个 512 维向量，学习者已反馈下标对应关系及向量与维度的区别。FAISS 内存建库示例已完成，助手运行确认索引维度为 512、向量数量为 3；学习者运行与建库概念理解待验收，问题检索尚未实现。
- 助手已通过 `curl` 和浏览器 `/docs` 验证 `GET /` 返回状态码 `200` 和 `{"Hello":"World"}`；学习者已说明应用对象、路由装饰器和处理函数的基本关系，验收记录见学习计划。
- 已有独立的 `src/llm_demo.py` 模型调用示例；文档检索、问答接口和 Docker 部署将在后续步骤中逐步实现。

任务勾选和学习记录统一维护在 [第一周学习计划](第一周学习计划.md) 中。

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [src/main.py](src/main.py) | FastAPI 应用入口，包含 Hello World、问候路由和接收 JSON 问题的接口 |
| [src/llm_demo.py](src/llm_demo.py) | 独立的 LCEL 示例，读取配置，通过模板、模型、解析器组成的 Chain 解释 `topic` 并打印字符串结果 |
| [data/notes.md](data/notes.md) | 第 3 天的 RAG 练习材料，记录当前项目中的路由、参数、请求体与校验 |
| [src/load_demo.py](src/load_demo.py) | 读取练习文档，创建包含正文和来源元数据的 `Document`，打印正文、元数据及字符数 |
| [src/split_demo.py](src/split_demo.py) | 将练习文档分块，打印文本块数量，以及前 3 块的正文、字符数与来源 |
| [src/embedding_demo.py](src/embedding_demo.py) | 在 CPU 上加载本地中文 Embedding 模型，将一句问题转换成向量，打印维度和前 5 个数值 |
| [src/embed_chunks_demo.py](src/embed_chunks_demo.py) | 将练习文档分块并批量向量化，按对应顺序打印每块正文、来源、向量维度和前 5 个数值 |
| [src/faiss_demo.py](src/faiss_demo.py) | 将文本块向量加入内存中的 FAISS 索引，打印维度、向量数量及编号与原文来源的对应关系 |
| [第一周学习计划.md](第一周学习计划.md) | 每日任务、验收标准、进度勾选和复盘记录 |
| [AGENTS.md](AGENTS.md) | AI 助手在本项目中的协作与开发约定 |
| [README.md](README.md) | 项目介绍、运行方法和学习入口 |

源码（包括学习示例脚本）统一放在项目根目录的 `src/` 下；练习文档放在 `data/`，`pyproject.toml`、`uv.lock`、本地 `.env` 和说明文档保留在根目录。下方所有命令均从项目根目录执行。

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
uv run fastapi dev src/main.py
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
uv run fastapi dev src/main.py
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
uv run --env-file .env python src/llm_demo.py
```

脚本使用 `ChatPromptTemplate` 定义“请用三句话解释什么是 {topic}。”，通过 `chain = prompt | llm | parser` 连接提示词模板、模型和 `StrOutputParser`。调用 `chain.invoke({"topic": "FastAPI"})` 后，依次填入主题、请求模型、将回复消息解析为正文字符串，最后打印正文及 `isinstance(result, str)` 的检查结果。当前 `topic` 为 `FastAPI`；修改 `chain.invoke(...)` 中的主题值后重新运行，即可复用同一条 Chain 解释其他概念。

学习者此前在逐步调用版本中提供了 `FastAPI` 和 `Pydantic` 两个主题的输出，并说明模板填充与模型请求的区别，提示词模板验收通过。加入解析器后，学习者提供了 Pydantic 的三句话解释和 `True`，并确认解析器只处理已有消息、不再次请求模型服务，解析器验收通过。LCEL 版本已由助手只读核对代码；学习者先后将同一条 Chain 的主题设为 `Pydantic` 和 `FastAPI`，两次均得到对应的三句话解释和 `True`，并已说明 `llm` 的输出交给 `parser`、组件通过统一接口组合，LCEL 基础理解及两主题复用均已验收，第 2 天完成。以上模型运行依据均为学习者提供的实际输出，助手未另行请求模型服务。

## 运行文档加载示例

在项目根目录执行：

```bash
uv run python src/load_demo.py
```

脚本根据自身路径找到项目根目录（`src/` 的上一级），再定位 `data/notes.md`，使用 Python 标准库 `pathlib` 以 UTF-8 读取正文，再创建 LangChain 的 `Document` 对象：`page_content` 保存正文，`metadata` 字典中的 `source` 保存文件的绝对路径。

预期输出为完整笔记、包含 `source` 的元数据字典，以及字符数；当前文档为 1322 个字符，包含 Markdown 标记、空格和换行。迁移至 `src/` 前，助手已使用项目的 `langchain-core` 1.7.3 环境执行 `uv run --no-sync python load_demo.py`，确认上述结果。学习者已准确说明 `page_content` 保存正文，`metadata` 保存来源等元数据，并提供当时的 `uv run python load_demo.py` 的完整输出，正文、来源路径和字符数均符合预期，文档加载这一步通过。

## 运行文档分块示例

在项目根目录执行：

```bash
uv run python src/split_demo.py
```

脚本重新读取练习文档并创建 `Document`，再使用 `RecursiveCharacterTextSplitter` 分块。当前参数为 `chunk_size=500`、`chunk_overlap=50`、`length_function=len`：按字符数计量块大小，目标重叠为 50 个字符。分割器优先沿段落、换行等位置切分，实际块长与重叠受切分位置影响。本次只把块大小从 300 调整为 500，用于比较内容边界。

`split_documents([document])` 接收文档列表，返回文本块的 `Document` 列表，并将原文档的元数据保留在块中。脚本打印总块数及前 3 块的正文、字符数和来源，便于观察分块边界。

在 `langchain-text-splitters` 1.1.3 环境中，同一份 1322 个字符的笔记有如下结果：

| 块大小 | 目标重叠 | 总块数 | 前 3 块字符数 | 验证依据 |
| --- | --- | --- | --- | --- |
| 300 | 50 | 6 | 182、279、293 | 助手运行与学习者实际输出 |
| 500（当前） | 50 | 3 | 463、466、388 | 助手运行；学习者已提供相同分块参数的文本块向量化完整输出 |

当前三块的来源均指向原笔记。原先第一块只包含根路由的说明，调整后第一块还包含问候路由和路径参数的说明；参数调整与两组内容边界的比较已完成。学习者已理解块大小上限，并识别只看到结论时可能缺少条件；块大小、重叠作用及内容相关性的基础概念已获得学习者确认，第 3 天完成。助手另行核对当前相邻块的首尾文字，两处实际连续重叠均为 0，不能仅凭 `chunk_overlap=50` 认定每对块都重复 50 个字符。

## 运行 Embedding 示例

在项目根目录执行：

```bash
uv run python src/embedding_demo.py
```

示例使用 `langchain_huggingface.HuggingFaceEmbeddings` 加载公开的中文模型 `BAAI/bge-small-zh-v1.5`，在本机 CPU 上计算，不需要 `.env` 或公司网关的 API 密钥。首次运行需要联网下载模型，文件保存在 Hugging Face 的本机缓存中；后续运行可以复用缓存。

当前输入是 `空字符串为什么返回 422？`。`embeddings.embed_query(text)` 将问题字符串编码为浮点数列表，脚本打印输入文本、`len(vector)` 和 `vector[:5]`。预期向量维度为 `512`，前 5 个数值用于观察结果；只展示 5 个数值不代表完整向量只有 5 维。

当前使用 `langchain-huggingface` 1.2.3 和 `sentence-transformers` 6.2.0，依赖已由 `uv add` 添加并记录在锁文件中；已核对 LangChain 官方接口文档和 BAAI 官方模型卡。助手已执行上述命令，确认模型加载成功，输出维度为 `512` 并打印 5 个浮点数；再使用 `HF_HUB_OFFLINE=1 uv run python src/embedding_demo.py` 验证本机缓存可用，输出一致。学习者已提供上述正常运行命令的完整输出，维度和前 5 个数值均一致，并准确说明 `vector[:5]` 只取前 5 个元素，运行与本轮基础理解验收均通过。

## 运行文本块向量化示例

在项目根目录执行：

```bash
uv run python src/embed_chunks_demo.py
```

脚本沿用文档分块示例的加载方式和参数（块大小 500、目标重叠 50），使用同一个 `BAAI/bge-small-zh-v1.5` 模型和 CPU、归一化配置。先通过 `texts = [chunk.page_content for chunk in chunks]` 按顺序取出各块正文，再调用 `vectors = embeddings.embed_documents(texts)`，为每段文字生成一个向量。

`chunks` 保存包含正文与来源的 `Document` 列表，`vectors` 保存对应的向量列表；`chunks[0]` 对应 `vectors[0]`，其余位置依此类推。脚本逐块打印正文、字符数、来源、向量维度和前 5 个数值，便于观察对应关系。当前结果只保存在本次运行的内存中。

助手已执行上述命令，确认文本块数量和向量数量均为 `3`，三块字符数仍为 `463`、`466`、`388`，每个向量维度均为 `512`，来源均指向 `data/notes.md` 的绝对路径。2026 年 11 月 3 日，学习者提供上述命令的完整输出，块数、向量数量、三块长度、维度及来源均符合预期，学习者运行已验证。下标从 0 开始：`chunks[1]` 是第二块的 `Document`，其正文为 `chunks[1].page_content`；`vectors[1]` 是该块的完整向量，`len(vectors[1])` 才是维度 `512`。学习者随后说明 `vectors[0]` 对应下标为 0 的块，`len(vectors[0])` 为 `512`；下标 0 对应终端打印的“第 1 块”。结合运行结果及本轮反馈，文本块向量化的基础理解验收通过；后续建库示例见下节。

## 运行 FAISS 建库示例

在项目根目录执行：

```bash
uv run python src/faiss_demo.py
```

脚本沿用文本块向量化示例的文档、分块参数、本地模型和 CPU、归一化配置，每次运行都会重新分块和计算向量。新增部分将向量列表转换成 NumPy 的 `float32` 二维数组，每行对应一个文本块，再创建 `faiss.IndexFlatL2(dimension)`，通过 `index.add(vector_array)` 按顺序加入向量。

预期关键输出：

```text
文本块数量： 3
向量数组形状： (3, 512)
向量数据类型： float32
索引维度： 512
索引中的向量数量： 3
```

`(3, 512)` 表示 3 行、512 列，即 3 个向量、每个向量有 512 个数值。`index.d` 是索引接受的向量维度，`index.ntotal` 是已经加入的向量数量。

本例将向量一次性按 `chunks` 的顺序加入空索引，编号从 0 开始。因此编号 `0` 对应 `chunks[0]`，编号 `1` 对应 `chunks[1]`，编号 `2` 对应 `chunks[2]`。正文与来源仍保存在 `chunks` 中，FAISS 索引负责保存向量；脚本逐项打印编号、正文前 80 个字符、块长和来源，以便核对对应关系。当前索引和文本块都只保存在本次运行的内存中，退出后不会保留；本轮尚未实现问题检索与索引持久化。

依赖已通过 `uv add faiss-cpu numpy` 配置，当前锁定版本分别为 1.15.1 和 2.5.4。已核对 FAISS 官方入门文档与本机版本的 `Index.add` 实现。运行时发现，在本机 macOS 环境中先导入 FAISS 再运行本地模型会发生底层崩溃；脚本因此在文本块向量化后导入 FAISS，调整后正常运行。

2026 年 11 月 3 日，助手执行上述运行命令成功，输出与预期一致，编号 `0、1、2` 对应的三块长度仍为 `463、466、388`，来源均指向练习文档。排查时还验证了调整导入顺序后的索引向量与原数组逐项一致，且加载 FAISS 后模型仍可再次编码问题。学习者运行、`index.d` 与 `index.ntotal` 的区别及编号对应关系的理解待验收。

## 本周目标

最终实现一个接收问题的 `POST /ask` 接口，根据本地 Markdown/TXT 文档生成答案，并返回检索到的参考片段与来源。

计划使用 FastAPI、Pydantic、LangChain 和 FAISS，最后通过 Docker 在本地运行。具体依赖在对应学习步骤中引入。

```text
建库：文档 → 加载 → 分块 → Embedding → FAISS 索引
问答：问题 → 检索相关片段 → 提示词 → 模型 → 答案与参考片段
```

## 学习节奏

每次安排 60–90 分钟，做不完就顺延。先理解当前小步骤的目标，再实现和验证；完成验收后继续下一项。

第 1–3 天均已完成基础验收。第 4 天的单句与文本块向量化均已通过；FAISS 内存建库示例的代码与助手运行验证已完成，学习者运行及建库概念理解待验收。当前下一步是运行建库示例并核对维度、数量和编号对应关系，完成后再学习问题检索。任务勾选和验收依据见 [第一周学习计划](第一周学习计划.md)。
