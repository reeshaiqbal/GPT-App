import os
import gradio as gr
import matplotlib
matplotlib.use("agg")
from openai import OpenAI

client = OpenAI(api_key="Put your API Key here")  #API key kept hidden due to security reasons

system_prompt = (
    "The following is a conversation with an AI assistant. "
    "The assistant is helpful, creative, clever, and friendly."
)

def chat_with_openai(message, history):
    history = history or []

    messages = [{"role": "system", "content": system_prompt}]
    for user_msg, ai_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.9
    )

    reply = response.choices[0].message.content

    history.append((message, reply))
    return history, history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg_box = gr.Textbox(placeholder="Type your message here…")
    state = gr.State()
    submit = gr.Button("Send")
    submit.click(chat_with_openai, inputs=[msg_box, state], outputs=[chatbot, state])

demo.launch(debug=True)
