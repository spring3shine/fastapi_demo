from fastapi import FastAPI, HTTPException
from starlette.responses import Response, HTMLResponse

from fastapi import WebSocket

from app.db.models import UserAnswer
from app.api import api

app = FastAPI()


# @app.get("/")
# def root():
#     return {"message": "Fast API in Python"}


@app.get("/user")
def read_user():
    return api.read_user()


@app.get("/question/{position}", status_code=200)
def read_questions(position: int, response: Response):
    question = api.read_questions(position)

    if not question:
        raise HTTPException(status_code=400, detail="Error")

    return question


@app.get("/alternatives/{question_id}")
def read_alternatives(question_id: int):
    return api.read_alternatives(question_id)


@app.post("/answer", status_code=201)
def create_answer(payload: UserAnswer):
    payload = payload.dict()

    return api.create_answer(payload)


@app.get("/result/{user_id}")
def read_result(user_id: int):
    return api.read_result(user_id)


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:10001/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # 接收客户端发送的消息
        import datetime
        import asyncio

        # print(datetime.datetime.now)
        await asyncio.sleep(3)
        now = datetime.datetime.now()
        # message = now.strftime("yyyy-MM-DD HH:mm:ss")
        message = "" + str(now)
        # message = await websocket.receive_text()
        print(message)
        # 将消息回传给客户端
        await websocket.send_text(message)
