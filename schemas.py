from pydantic import BaseModel


class ConfigSchema(BaseModel):
    user_id: int
    api_id: int
    api_hash: str
    bot_token: str
    string_session: str
