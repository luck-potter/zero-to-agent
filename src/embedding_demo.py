from langchain_huggingface import HuggingFaceEmbeddings

model_name = "BAAI/bge-small-zh-v1.5"
text = "空字符串为什么返回 422？"

print("加载模型：", model_name, flush=True)
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vector = embeddings.embed_query(text)

print("输入文本：", text)
print("向量维度：", len(vector))
print("前 5 个数值：", vector[:5])
