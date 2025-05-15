from pydantic import BaseModel
from db_service import get_db, save_db
import questionary
import uuid

NEW_THREAD = "New thread"
THREADS = "threads"


# models
class Thread(BaseModel):
    id: str
    name: str


# services
def get_threads():
    return get_db().get(THREADS)


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
