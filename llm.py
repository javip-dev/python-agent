from dotenv import load_dotenv
from openai import OpenAI
from enum import Enum


load_dotenv()

client = OpenAI()


class Tools(Enum):
    WEB_SEARCH = "web_search_preview"


class Llm:
    def __init__(self, model="gpt-4o-mini"):
        self.client = client
        self.instructions = ""
        self.model = model
        self.tools = None

    def set_instructions(self, instructions: str):
        self.instructions = instructions

    def set_tools(self):
        self.tools = [{"type": Tools.WEB_SEARCH.value}]

    def ask(self, input):
        if not input:
            print("must provide a question")
            return

        return self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            tools=self.tools,  # type: ignore
            input=input,
        )
