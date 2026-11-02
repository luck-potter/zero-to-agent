from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os

llm = ChatOpenAI(
    model=os.environ["LLM_MODEL"],
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)
prompt = ChatPromptTemplate.from_template("请用三句话解释什么是 {topic}。")


prompt_value = prompt.invoke({"topic": "Pydantic"})

response = llm.invoke(prompt_value)

print(response.text)