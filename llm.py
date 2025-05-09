import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class Llm:
    def __init__(self, model="gpt-4o-mini"):
        self.client = client
        self.instructions = ""
        self.model = model

    def set_instructions(self, instructions: str):
        self.instructions = instructions

    def ask(self, input: str):
        if not input:
            print("must provide a question")
            return
        response = self.client.responses.create(
            model=self.model,
            instructions=self.instructions,
            input=input,
        )

        print(response.output_text)
