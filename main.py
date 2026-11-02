from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello/{name}")
def say_hello(name: str, language: str = "en"):
    if language == "en":
        return {"message": f"Hello, {name}!"}
    return {"message": f"你好，{name}！"}