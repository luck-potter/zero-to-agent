from pathlib import Path

from langchain_core.documents import Document
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

print("原文字符数：", len(document.page_content))
print("文本块数量：", len(chunks))

for index, chunk in enumerate(chunks[:3], start=1):
    print(f"\n第 {index} 块：")
    print(chunk.page_content)
    print("字符数：", len(chunk.page_content))
    print("来源：", chunk.metadata["source"])
