from pyrogram import *
from json import load

import pyrogram
import utils
def start_client(session: "utils.Session"):
    return Client(name="MyApp", api_id=session.api_id, api_hash=session.api_hash, bot_token=session.bot_token)

