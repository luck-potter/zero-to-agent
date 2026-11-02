from pathlib import Path

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

# 从每个 Document 中取出正文，按原顺序组成字符串列表。
texts = [chunk.page_content for chunk in chunks]
vectors = embeddings.embed_documents(texts)

print("文本块数量：", len(chunks))
print("向量数量：", len(vectors))

for index, chunk in enumerate(chunks):
    # 相同下标对应同一块：chunks[0] 的向量是 vectors[0]。
    vector = vectors[index]
    print(f"\n第 {index + 1} 块：")
    print(chunk.page_content)
    print("字符数：", len(chunk.page_content))
    print("来源：", chunk.metadata["source"])
    print("向量维度：", len(vector))
    print("前 5 个数值：", vector[:5])
