import sys
from llm import Llm


def main():

    if len(sys.argv) != 2:
        print("no arguments have been passed")
        sys.exit(1)

    llm = Llm()
    llm.set_instructions("You are a coding assistant that talks like a pirate.")
    llm.ask(sys.argv[1])


main()
