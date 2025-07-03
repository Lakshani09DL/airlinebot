import gradio as gr
import asyncio
from router import handle_query_gradio

# Async response handler
async def async_chat(user_input, history):
    return await handle_query_gradio(user_input)

def chat_interface(user_input, history):
    return asyncio.run(async_chat(user_input, history))

def respond(user_input, history):
    response = chat_interface(user_input, history)
    history.append((user_input, response))
    return "", history

# Build the UI
with gr.Blocks(css="""
body {
    background: linear-gradient(to right, #dbeafe, #e0f2fe);
    font-family: 'Segoe UI', sans-serif;
}

#title {
    text-align: center;
    font-size: 28px;
    color: #1e3a8a;
    margin-top: 1em;
    margin-bottom: 0.5em;
}

#chatbot .message.user {
    background-color: #bfdbfe !important;
    border-radius: 12px;
    padding: 10px 14px;
    margin: 6px;
    max-width: 75%;
    align-self: flex-end;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

#chatbot .message.bot {
    background-color: #ffffff !important;
    border-radius: 12px;
    padding: 10px 14px;
    margin: 6px;
    max-width: 75%;
    align-self: flex-start;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

button {
    background-color: #3b82f6 !important;
    color: white !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-weight: bold;
    margin-top: 4px;
}

button:hover {
    background-color: #2563eb !important;
}
""") as demo:

    gr.Markdown("## 🛫 Airline Customer Service Bot", elem_id="title")
    chatbot = gr.Chatbot(elem_id="chatbot", height=400)

    with gr.Row():
        msg = gr.Textbox(
            show_label=False,
            placeholder="Ask me about flights, baggage, bookings, or complaints...",
            scale=4
        )
        submit_btn = gr.Button("✈️ Send", scale=1)

    clear_btn = gr.Button("🧹 Clear Chat")

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear_btn.click(lambda: [], None, chatbot)

if __name__ == "__main__":
    demo.launch()
