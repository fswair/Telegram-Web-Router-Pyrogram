import config
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Response, Request
from iotypes import Raw, Methods
from uvicorn import run
from utils import async_execute, JSON, Form, Config
from pyrogram.types import Message
from pyrogram import Client
from schemas import ConfigSchema
from database import db

app = FastAPI()

bot_config = Config().get_session()


@app.get("/api/methods/get_users", response_class=JSONResponse)
async def get_users(user_ids: int | str = "me"):
    if user_ids:
        seperator = ","
        if seperator in user_ids:
            user_ids = user_ids.split(seperator)
        response = await async_execute(
            config=bot_config, method=Methods.GET_USERS, user_ids=user_ids
        )
        return response
    return dict(code=404, message="Invalid Params.")


@app.get("/api/methods/get_me", response_class=JSONResponse)
async def get_users():
    response = await async_execute(config=config.BOT)
    return JSON(response)


@app.get("/api/methods/send_message", response_class=JSONResponse)
async def get_users(chat_id: int | str, text: str, delay: int = 1, times: int = None):
    if not delay:
        delay = 1
    if times:
        datas = []
        for x in range(times):
            response = await async_execute(
                config=bot_config,
                method=Raw.MESSAGES.SEND.MESSAGE,
                chat_id=chat_id,
                text=text,
            )
            data: dict = JSON(response)
            data.update(
                {
                    "id": {
                        "message": {
                            "id": data.get("id"),
                            "methods": {
                                "edit": f"/api/raw/messages/edit/{data.get('id')}?chat_id={data.get('chat').get('id')}&text=",
                                "delete": f"/api/raw/messages/delete/{data.get('id')}",
                            },
                        }
                    }
                }
            )
            datas.append(data)
        return datas
    response = await async_execute(
        config=bot_config,
        method=Raw.MESSAGES.SEND.MESSAGE,
        chat_id=chat_id,
        text=text,
    )
    data: dict = JSON(response)
    data.update(
        {
            "id": {
                "message": {
                    "id": data.get("id"),
                    "methods": {
                        "edit": f"/api/raw/messages/edit/{data.get('id')}?chat_id={data.get('chat').get('id')}&text=",
                        "delete": f"/api/raw/messages/delete/{data.get('id')}",
                    },
                }
            }
        }
    )

    return data


@app.get("/api/raw/messages/edit/{message_ids}")
async def edit_message(
    message_ids: int, chat_id: str | int, text: str, response: Response
):
    message: Message = await async_execute(
        config=bot_config,
        method=Raw.MESSAGES.GET.MESSAGE,
        message_ids=message_ids,
        chat_id=chat_id,
    )
    edited_message: Message = await async_execute(
        config=bot_config,
        method=Raw.MESSAGES.EDIT.MESSAGE,
        chat_id=chat_id,
        message_id=message_ids,
        text=text,
    )

    return JSON(edited_message)


@app.post("/create")
async def post(request: Request):
    model: ConfigSchema = Form(await request.form())
    config = Config()
    config.api_hash = model.api_hash
    config.api_id = model.api_id
    config.bot_token = model.bot_token
    try:
        async with Client(
            name=f"{config.api_id}_session",
            api_id=config.api_id,
            api_hash=config.api_hash,
            bot_token=config.bot_token,
            in_memory=True,
        ) as cli:
            me = cli.get_me()
            config.user_id = me.id
            config.insert()
            return db.select("sessions", where=dict(api_id=model.api_id))
    except:
        return dict(code=403, message="Invalid Authorization.")


run(app="api:app", host=config.BUILD.HOST, port=config.BUILD.PORT, reload=True)
