from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

llm = ChatOpenAI(
    model=os.environ["LLM_MODEL"],
    base_url=os.environ["OPENAI_BASE_URL"],
    api_key=os.environ["OPENAI_API_KEY"],
)
prompt = ChatPromptTemplate.from_template("请用三句话解释什么是 {topic}。")
parser = StrOutputParser()


chain = prompt | llm | parser
result = chain.invoke({"topic": "FastAPI"})
print(result)
print(isinstance(result, str))