import json
import sys
from llm import Llm
from utils import user_msg, assistant_msg


def main():

    if len(sys.argv) != 2:
        print("no arguments have been passed")
        sys.exit(1)

    llm = Llm()
    llm.set_instructions("you are a sport focus commentator")
    # llm.set_tools()
    msg = user_msg(sys.argv[1])
    response = llm.ask(msg)
    if response is None:
        sys.exit(1)
    print(response.output_text)
    assistant_msg(response.output_text)


main()
