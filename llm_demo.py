from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model=os.environ["LLM_MODEL"],
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)

response = llm.invoke("请用三句话解释什么是 FastAPI。")

print(response.text)