from pathlib import Path

import numpy as np
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

file_path = Path(__file__).resolve().parent.parent / "data" / "notes.md"
text = file_path.read_text(encoding="utf-8")
document = Document(
    page_content=text,
    metadata={"source": str(file_path)},
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    length_function=len,
)
chunks = splitter.split_documents([document])

model_name = "BAAI/bge-small-zh-v1.5"
print("加载模型：", model_name, flush=True)
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

texts = [chunk.page_content for chunk in chunks]
vectors = embeddings.embed_documents(texts)

# 本机 macOS 环境先导入 FAISS 再运行模型会崩溃，因此在向量化后导入。
import faiss

# 一行是一个文本块的向量；转换为 FAISS 使用的 float32 数组。
vector_array = np.array(vectors, dtype="float32")
dimension = vector_array.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(vector_array)

print("文本块数量：", len(chunks))
print("向量数组形状：", vector_array.shape)
print("向量数据类型：", vector_array.dtype)
print("索引维度：", index.d)
print("索引中的向量数量：", index.ntotal)

# 本例一次性按 chunks 的顺序加入向量，因此索引编号对应 chunks 的下标。
# 正文和来源仍保存在 chunks 中；本轮索引只保存在内存中。
for chunk_id, chunk in enumerate(chunks):
    print(f"\n索引编号 {chunk_id} → 第 {chunk_id + 1} 块")
    print("正文预览：", chunk.page_content[:80])
    print("字符数：", len(chunk.page_content))
    print("来源：", chunk.metadata["source"])
