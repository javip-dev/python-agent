import sys
from llm import Llm
from message_service import user_msg, assistant_msg
from thread_service import get_thread_id
from utils import print_output
import questionary


def main():

    thread_id = get_thread_id()
    if not thread_id:
        sys.exit(1)

    llm = Llm()
    llm.set_instructions("you are a sport focus commentator")
    print("what can i help with?")
    while True:
        user_input = questionary.text("").ask()
        if user_input == "END":
            sys.exit(1)
        print(user_input)
        # llm.set_tools()
        llm_input = user_msg(user_input, thread_id)
        response = llm.ask(llm_input)
        if response is None:
            sys.exit(1)
        assistant_msg(response.output_text, thread_id)
        print_output(response.output_text)


main()
