import sys
from llm import Llm
from message_service import user_msg, assistant_msg
from thread_service import get_thread_id
from instructions_service import get_prompt
from utils import print_output
import questionary


def main():
    if len(sys.argv) == 2:
        model = sys.argv[1]

    thread_id = get_thread_id()
    if not thread_id:
        sys.exit(1)

    prompt = get_prompt(thread_id)
    llm = Llm(model)
    llm.set_instructions(prompt)
    # llm.set_tools()
    print("what can i help with?")
    while True:
        user_input = questionary.text("").ask()
        if user_input == "END":
            sys.exit(1)
        llm_input = user_msg(user_input, thread_id)
        response = llm.ask(llm_input)
        if response is None:
            sys.exit(1)
        assistant_msg(response.output_text, thread_id)
        print_output(response.output_text)


main()
