from enum import Enum
import json
from typing import List
import uuid
from datetime import datetime
from openai.types.responses.response_output_item import ResponseOutputItem
from openai.types.responses.response_output_message import ResponseOutputMessage


DB = "db.json"


class ROLES(Enum):
    USER = "user"
    ASSISTANT = "assistant"


def add_metada(ai_msg: str, role: ROLES):
    now = datetime.now()
    ts = int(now.timestamp())
    return {
        "role": role.value,
        "content": ai_msg,
        "created_at": ts,
        "id": str(uuid.uuid4()),
    }


def remove_metada(ai_msg):
    return {
        "role": ai_msg.get("role"),
        "content": ai_msg.get("content"),
    }


def user_msg(msg: str):
    save_db(msg, ROLES.USER)
    return get_db()


def assistant_msg(msg: str):
    save_db(msg, ROLES.ASSISTANT)


def get_db():
    with open(DB, "r") as file:
        data = json.load(file)
    return list(map(remove_metada, data.get("messages")))


def save_db(msg: str, role: ROLES):
    with open(DB, "r") as file:
        data = json.load(file)
    history = list(data.get("messages"))
    message = add_metada(msg, role)
    history.append(message)
    database = {"messages": history}
    with open(DB, "w") as outfile:
        json_string = json.dumps(database, indent=2)
        outfile.write(json_string)


# def store_msg(
#     output_text: str,
# ):
#     with open(DB, "r") as file:
#         data = json.load(file)
#     history = list(data.get("messages"))
#     history.append(add_metada(output_text))
#     database = {"messages": history}

#     with open(DB, "w") as outfile:
#         json_string = json.dumps(database, indent=2)
#         outfile.write(json_string)


# from openai import OpenAI

# client = OpenAI()

# history = [
#     {
#         "role": "user",
#         "content": "tell me a joke"
#     }
# ]

# response = client.responses.create(
#     model="gpt-4o-mini",
#     input=history,
#     store=False
# )

# print(response.output_text)

# # Add the response to the conversation
# history += [{"role": el.role, "content": el.content} for el in response.output]

# history.append({ "role": "user", "content": "tell me another" })

# second_response = client.responses.create(
#     model="gpt-4o-mini",
#     input=history,
#     store=False
# )

# print(second_response.output_text)
