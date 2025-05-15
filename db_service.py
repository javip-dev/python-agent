from enum import Enum
import json
import uuid
from datetime import datetime
import questionary
from pydantic import BaseModel

# from openai.types.responses.response_output_item import ResponseOutputItem
# from openai.types.responses.response_output_message import ResponseOutputMessage

# consts

DB = "db.json"
NEW_THREAD = "New thread"
THREADS = "threads"
MESSAGES = "messages"


# models
class Thread(BaseModel):
    id: str
    name: str


class ROLES(Enum):
    USER = "user"
    ASSISTANT = "assistant"


# db interaction


def get_db():
    with open(DB, "r") as file:
        db = json.load(file)
    return db


def save_db(db):
    with open(DB, "w") as outfile:
        json_string = json.dumps(db, indent=2)
        outfile.write(json_string)


def get_threads():
    return get_db().get(THREADS)


def get_messages(thread_id):
    messages = list(
        filter(lambda msg: msg["thread_id"] == thread_id, get_db().get(MESSAGES))
    )
    messages.sort(key=lambda m: m["created_at"])
    return list(map(remove_metada, messages))


def get_thread_id() -> str:
    threads = get_threads()
    thread_names = [NEW_THREAD] + [thread["name"] for thread in threads]
    t_name = questionary.select("Chose a thread", choices=thread_names).ask()
    if t_name == NEW_THREAD:
        name = input("Chose a name for the new thread ")
        thread = save_new_thread(name)
        return thread.id
    thread = next((thread for thread in threads if thread["name"] == t_name))
    return thread["id"]


def save_thread(thread: Thread):
    db = get_db()
    threads = db.get(THREADS)
    threads.append(thread.__dict__)
    db[THREADS] = threads
    save_db(db)


def save_new_thread(name: str) -> Thread:
    new_t = {"name": name, "id": str(uuid.uuid4())}
    thread: Thread = Thread(**new_t)
    save_thread(thread)
    return thread


def save_message(message):
    db = get_db()
    messages = db.get(MESSAGES)
    messages.append(message)
    db[MESSAGES] = messages
    save_db(db)


# service


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
