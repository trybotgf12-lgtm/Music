from pyrogram.enums import ChatMemberStatus

from config import SUDO_USERS
from database import is_approved


async def is_authorized(client, chat_id: int, user_id: int) -> bool:
    if user_id in SUDO_USERS:
        return True

    if await is_approved(chat_id, user_id):
        return True

    try:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER)
    except Exception:
        return False
