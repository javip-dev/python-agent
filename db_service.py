import json

# from openai.types.responses.response_output_item import ResponseOutputItem
# from openai.types.responses.response_output_message import ResponseOutputMessage

# consts

DB = "db.json"


# db interaction
def get_db():
    with open(DB, "r") as file:
        db = json.load(file)
    return db


def save_db(db):
    with open(DB, "w") as outfile:
        json_string = json.dumps(db, indent=2)
        outfile.write(json_string)
