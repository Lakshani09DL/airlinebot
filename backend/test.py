from router import router_chain

print("=== Airline Customer Service Bot (Gemini) ===")
print("Type your query below. Type 'exit' or 'quit' to stop.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting...")
        break

    # Run the input through your router chain
    response = router_chain.run(user_input)
    print("Bot:", response)
    print("-" * 40)
