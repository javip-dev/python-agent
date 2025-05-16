import uuid
from pydantic import BaseModel
from db_service import get_db, save_db

INSTRUCTIONS = "instructions"


class Instruction(BaseModel):
    id: str
    thread_id: str
    prompt: str


def get_instructions():
    return get_db().get(INSTRUCTIONS)


def get_prompt(thread_id) -> str:
    instructions = get_instructions()
    return next(
        (
            instruction.get("prompt")
            for instruction in instructions
            if instruction.get("thread_id") == thread_id
        )
    )


def save_instructions(txt: str, thread_id: str):
    db = get_db()
    id = str(uuid.uuid4())
    instructions = db.get(INSTRUCTIONS)
    new_i = {"id": id, "prompt": txt, "thread_id": thread_id}
    instruction = Instruction(**new_i)
    instructions.append(instruction.__dict__)
    db[INSTRUCTIONS] = instructions
    save_db(db)
