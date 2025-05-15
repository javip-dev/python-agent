from datetime import datetime
from enum import Enum
import uuid
from db_service import get_db, save_db

# consts
MESSAGES = "messages"


# models
class ROLES(Enum):
    USER = "user"
    ASSISTANT = "assistant"


# services
def get_messages(thread_id):
    messages = list(
        filter(lambda msg: msg["thread_id"] == thread_id, get_db().get(MESSAGES))
    )
    messages.sort(key=lambda m: m["created_at"])
    return list(map(remove_metada, messages))


def save_message(message):
    db = get_db()
    messages = db.get(MESSAGES)
    messages.append(message)
    db[MESSAGES] = messages
    save_db(db)


def user_msg(msg: str, thread_id: str):
    message = add_metada(msg, ROLES.USER, thread_id)
    save_message(message)
    return get_messages(thread_id)


def assistant_msg(msg: str, thread_id: str):
    message = add_metada(msg, ROLES.ASSISTANT, thread_id)
    save_message(message)


# utils
def add_metada(ai_msg: str, role: ROLES, thread_id):
    now = datetime.now()
    ts = int(now.timestamp())
    return {
        "role": role.value,
        "content": ai_msg,
        "created_at": ts,
        "id": str(uuid.uuid4()),
        "thread_id": thread_id,
    }


def remove_metada(ai_msg):
    return {
        "role": ai_msg.get("role"),
        "content": ai_msg.get("content"),
    }
