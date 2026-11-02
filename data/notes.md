# FastAPI 学习笔记

## 路由：请求如何找到处理函数

在本项目中，`app = FastAPI()` 创建 Web 应用对象。`@app.get("/")` 把 `GET /` 请求关联到下方的 `read_root()` 函数。这个函数返回 Python 字典 `{"Hello": "World"}`，FastAPI 将它转换为 JSON 响应。

`@app.get("/hello/{name}")` 把问候请求关联到 `say_hello()` 函数。例如，访问 `/hello/xuzhi` 时，函数收到的 `name` 是字符串 `"xuzhi"`，返回的问候语会包含这个名字。

装饰器是会执行的 Python 代码，用来注册路由。路由函数负责处理匹配到的请求，并返回结果。

## 参数：路径参数和查询参数

路径参数是 URL 路径的一部分。在 `/hello/xuzhi` 中，路径参数名是 `name`，值是 `xuzhi`。把路径中的名字改为 `Alice`，响应里的名字也会随之改变。

查询参数写在 URL 的 `?` 后面，使用 `参数名=值` 的形式。在 `/hello/xuzhi?language=zh` 中，`language` 是查询参数名，`zh` 是它的值；路径参数 `name` 的值仍然是 `xuzhi`。

本项目中，`language` 的默认值是 `"en"`。访问 `/hello/xuzhi` 或 `/hello/xuzhi?language=en`，都会得到 `{"message":"Hello, xuzhi!"}`；访问 `/hello/xuzhi?language=zh`，会得到 `{"message":"你好，xuzhi！"}`。

当前问候接口只有在 `language` 等于 `"en"` 时返回英文，其余字符串都返回中文，尚未限制可选的语言值。

## 请求体与校验：提交一个问题

`POST /questions` 通过请求体接收 JSON。请求体由客户端发送给 FastAPI 服务，响应体由服务返回给客户端；使用 `/docs` 调试时，浏览器页面就是客户端。

请求模型 `QuestionRequest` 包含两个字段：`question` 是必填字符串，`language` 是默认值为 `"en"` 的字符串。`question` 使用 `Field(min_length=1)` 设置最小长度，因此不能省略，也不能是空字符串 `""`。

提交 `{"question":"什么是 FastAPI？","language":"zh"}` 时，接口返回状态码 `200`，响应体原样返回这两个字段。提交 `{"question":"什么是 FastAPI？"}` 时，响应中的 `language` 使用默认值 `"en"`。

提交 `{}` 会因为缺少 `question` 返回 `422`；提交 `{"question":""}` 会因为字符串长度不足返回 `422`。当前接口只接收并返回问题与语言，尚未调用模型生成答案。
