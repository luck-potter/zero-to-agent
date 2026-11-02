from pathlib import Path

from langchain_core.documents import Document

file_path = Path(__file__).resolve().parent.parent / "data" / "notes.md"
text = file_path.read_text(encoding="utf-8")

document = Document(
    page_content=text,
    metadata={"source": str(file_path)},
)

print("正文：")
print(document.page_content)
print("元数据：", document.metadata)
print("字符数：", len(document.page_content))
