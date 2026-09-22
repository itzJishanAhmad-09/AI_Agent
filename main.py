from agent import Agent

def main():
    agent = Agent()
    print("Agent ready. Type 'exit' to quit.\n")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in ("exit", "quit"):
            break
        if not user.strip():
            continue
        agent.run(user)

if __name__ == "__main__":
    main()