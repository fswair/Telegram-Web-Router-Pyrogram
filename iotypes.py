from pyrogram import Client as c
from pyrogram.types import Message as msg

### TYPE ENUMS ###
class Types:
    CREATED = 0
    STARTED = 1
    CONNECTED = 2


class Methods:
    """General Methods"""

    GET_ME = c.get_me.__name__
    GET_USERS = c.get_users.__name__


class GetChatStuff:
    """GET statement for CHATS."""

    CHAT_BASE = c.get_chat.__name__
    MEMBER = c.get_chat_member.__name__
    MEMBERS = c.get_chat_members.__name__
    MEMBERS_COUNT = c.get_chat_members_count.__name__
    HISTORY = c.get_chat_history.__name__
    HISTORY_COUNT = c.get_chat_history_count.__name__


class DeleteChatStuff:
    """DELETE statement for CHATS."""

    INVITE_LINKS = c.delete_chat_admin_invite_links.__name__
    INVITE_LINK = c.delete_chat_invite_link.__name__


class EditChatStuff:
    """EDIT statement for CHATS."""

    INVITE_LINK = c.edit_chat_invite_link.__name__


class Chat:
    GET = GetChatStuff()
    DELETE = DeleteChatStuff()
    EDIT = EditChatStuff()


class Get:
    MESSAGE = c.get_messages.__name__
    CHAT = Chat()


class Edit:
    MESSAGE = c.edit_message_text.__name__


class Delete:
    MESSAGE = c.delete_messages.__name__


class Send:
    MESSAGE = c.send_message.__name__
    DOCUMENT = c.send_message.__name__
    PHOTO = c.send_photo.__name__
    VIDEO = c.send_video.__name__
    AUDIO = c.send_audio.__name__


class RawMessages:
    GET = Get()
    EDIT = Edit()
    DELETE = Delete()
    SEND = Send()


class Raw:
    MESSAGES = RawMessages()


# example;
# Raw.MESSAGES.GET.CHAT.GET.HISTORY
