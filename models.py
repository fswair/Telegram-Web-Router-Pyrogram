from MentoDB import *


@dataclass
class ConfigModel(BaseModel):
    user_id: int
    api_id: int
    api_hash: str
    bot_token: str
    string_session: str
