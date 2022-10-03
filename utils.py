import json
from pyrogram import Client
from iotypes import Methods
from MentoDB import *
from database import db

JSON = lambda data: json.loads(str(data))


class Config:
    def __init__(
        self,
        user_id: int = 0,
        api_id: int = 0,
        api_hash: str = "",
        bot_token: str = "",
        string_session: str = "",
    ):
        self.user_id: int = user_id
        self.api_id: int = api_id
        self.api_hash: str = api_hash
        self.bot_token: str = bot_token
        self.string_session: str = string_session

    def insert(self):
        db.insert(
            "sessions",
            data=dict(
                user_id=self.user_id,
                api_id=self.api_id,
                api_hash=self.api_hash,
                bot_token=self.bot_token,
                string_session=self.string_session,
            ),
        )

    def get_session(self):
        sessions = db.select("sessions")
        if sessions:
            session = sessions[0]
            session = dict((k, v) for k, v in session.items() if not k == "user_id")
            return session
        return dict(name="Session")


async def async_execute(
    config: dict, method: Methods = Methods.GET_ME, *args, **kwargs
):
    async with Client(**config, in_memory=True) as client:
        job = client.__getattribute__(method)
        data = await job(*args, **kwargs)
        return data


class Response:
    __name__ = "response"


class Form:
    def __new__(cls, form_data: dict):
        form = dict(form_data)
        base = Response()
        for k, v in form.items():
            setattr(base, k, v)
        return base
