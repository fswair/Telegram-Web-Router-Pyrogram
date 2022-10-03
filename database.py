from models import ConfigModel
from MentoDB import Mento, MentoConnection

connection = MentoConnection(database="./database/sessions.db")

db = Mento(connection)

db.create(table="sessions", model=ConfigModel)
