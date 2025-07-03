import os
import asyncio
from config import GOOGLE_API_KEY
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI


os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)

# 1. Router Prompt
router_prompt = PromptTemplate.from_template("""
You are a smart intent classifier. Given a user query, classify it into one of these categories:

flight_status: Flight status queries
baggage_policy: Baggage rules and fees
booking_help: Bookings and ticket changes
complaints: Complaints and customer service issues

User Query: {input}

Reply with exactly one category key: flight_status, baggage_policy, booking_help, complaints
""")

router_chain = router_prompt | llm

intent_prompts = {
    "flight_status": PromptTemplate.from_template(
        """You are an airline assistant. A user wants to know the status of a flight.

Politely explain that live flight status isn't available here, and direct them to check it on the official website:

➡️ https://www.exampleairline.com/flight-status

User query: {input}

Keep your response short, polite, and helpful."""
    ),

    "baggage_policy": PromptTemplate.from_template(
        """You are an airline customer support assistant answering baggage policy questions.

Politely provide the core rules:
- Carry-on: 1 bag (max 7kg)
- Checked: 2 bags (max 23kg each)
- Oversize/extra baggage: charges apply

For full details, direct the user to:
➡️ https://www.exampleairline.com/baggage-policy

User query: {input}

Be clear and use bullet points."""
    ),

    "booking_help": PromptTemplate.from_template(
        """You are an airline booking assistant. A customer needs help with booking or changing a ticket.

Guide them to:
- Website: https://www.exampleairline.com
- Hotline: +94 11 234 5678
- Airport counter

User query: {input}

Be helpful and specific, and include available contact options."""
    ),

    "complaints": PromptTemplate.from_template(
        """You are a customer service agent handling airline complaints.

Apologize politely, acknowledge their concern, and guide them to submit a formal complaint here:
➡️ https://www.exampleairline.com/complaints

User query: {input}

Be professional, empathetic, and offer a clear next step."""
    )
}

# 3. Create runnable sequences for each intent
intent_chains = {
    intent: prompt | llm for intent, prompt in intent_prompts.items()
}

# 4. Main bot logic
async def run_bot(user_input: str) -> str:
    # Get the classified intent
    intent_msg = await router_chain.ainvoke({"input": user_input})
    intent = intent_msg.content.strip().lower()
    print(f"[Detected intent]: {intent}")

    # Route to correct intent chain
    if intent in intent_chains:
        response_msg = await intent_chains[intent].ainvoke({"input": user_input})
        return response_msg.content.strip()
    else:
        return "Sorry, I didn't understand your request. Please ask about flight status, baggage, bookings, or complaints."


async def main():
    print("✈️ Airline Assistant (Type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]:
            break
        response = await run_bot(query)
        print("Bot:", response)

async def handle_query_gradio(user_input: str) -> str:
    intent_msg = await router_chain.ainvoke({"input": user_input})
    intent = intent_msg.content.strip().lower()

    if intent in intent_chains:
        response_msg = await intent_chains[intent].ainvoke({"input": user_input})
        return response_msg.content.strip()
    else:
        return "Sorry, I couldn't understand your request. Please ask about flight status, baggage, bookings, or complaints."

if __name__ == "__main__":
    asyncio.run(main())
