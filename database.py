import motor.motor_asyncio

from config import MONGO_URL

_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL) if MONGO_URL else None
_db = _client["music_bot"] if _client else None

users_col = _db["users"] if _db is not None else None
chats_col = _db["chats"] if _db is not None else None
approved_col = _db["approved"] if _db is not None else None


async def add_user(user_id: int):
    if users_col is None:
        return
    await users_col.update_one({"_id": user_id}, {"$set": {"_id": user_id}}, upsert=True)


async def add_chat(chat_id: int):
    if chats_col is None:
        return
    await chats_col.update_one({"_id": chat_id}, {"$set": {"_id": chat_id}}, upsert=True)


async def get_all_users() -> list[int]:
    if users_col is None:
        return []
    return [doc["_id"] async for doc in users_col.find({})]


async def get_all_chats() -> list[int]:
    if chats_col is None:
        return []
    return [doc["_id"] async for doc in chats_col.find({})]


async def approve_user(chat_id: int, user_id: int):
    if approved_col is None:
        return
    await approved_col.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"chat_id": chat_id, "user_id": user_id}},
        upsert=True,
    )


async def unapprove_user(chat_id: int, user_id: int):
    if approved_col is None:
        return
    await approved_col.delete_one({"chat_id": chat_id, "user_id": user_id})


async def is_approved(chat_id: int, user_id: int) -> bool:
    if approved_col is None:
        return False
    doc = await approved_col.find_one({"chat_id": chat_id, "user_id": user_id})
    return doc is not None
