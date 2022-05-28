from datetime import datetime
import re
from pyrogram import Client, filters, enums
from sqlite3 import connect
import bot

database = connect("sessions.db", check_same_thread=False)
cursor = database.cursor()

class Request:
    def __init__(self, method: str):
        self.POST    : str = bool(re.match("post|POST|Post", method))
        self.GET     : str = bool(re.match("get|GET|Get", method))
        self.method  : str = "POST" if self.POST else ("GET" if self.GET else None)

class Session:
    def __init__(self, ip: str = None, datetime: datetime = datetime.now(), api_id: int = 0, api_hash: str = "", bot_token: str = "", is_active: int = 0):
        self.ip = ip
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.date = datetime
        self.timestamp = datetime.timestamp()
        self.is_active = is_active
        self.has_session = bool(self.is_active)
    def create(self):
        cursor.execute("CREATE TABLE IF NOT EXISTS sessions (id int, ip_address text, api_id int, api_hash text, bot_token text, date text, timestamp int, is_active int)")
        database.commit()
    def insert(self):
        cursor.execute(f"INSERT INTO sessions VALUES ({int(self.timestamp + self.api_id)}, '{self.ip}', {self.api_id}, '{self.api_hash}', '{self.bot_token}','{self.date}', {int(self.timestamp)}, {self.is_active})")
        database.commit()
    def get(self, ip_address: str = None) -> "Session":
        if not ip_address and not self.ip:
            return self
        else:
            current_ip = self.ip if not ip_address else ip_address
            user_sessions = cursor.execute(f"SELECT * FROM sessions where ip_address = '{current_ip}' ORDER BY -timestamp").fetchall()
            if len(user_sessions) > 0:
                ip, api_id, api_hash, bot_token, date, timestamp, is_active = user_sessions[0][1:]
                return Session(ip=ip, datetime=datetime.fromtimestamp(timestamp), api_id=api_id, api_hash=api_hash, bot_token=bot_token, is_active=is_active)
            else:
                return self

            return user_sessions
    def update(self) -> "Session":
        query = "ip_address = '{}', api_id = {}, api_hash = '{}', bot_token = '{}', date = '{}', timestamp = {}, is_active = {}".format(
            self.ip,
            self.api_id,
            self.api_hash, 
            self.bot_token,
            self.date,
            self.timestamp,
            self.is_active
        )
        cursor.execute(f"UPDATE sessions SET {query} where ip_address = '{self.ip}'")
        database.commit()

        return self.get()