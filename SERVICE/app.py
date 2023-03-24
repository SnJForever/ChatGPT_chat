from fastapi import FastAPI
import requests
import gradio as gr
import uvicorn


app = FastAPI()

@app.get("/gpt3")
def get_gpt3_results(prompt: str):
    print(prompt)
    headers = {
        "Authorization": "Bearer xxxx",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 100,
        "temperature": 0.7,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0].message.content.trim()
    else:
        return {"error": "Failed to get GPT-3.5-turbo results."}

@app.get("/dalle2")
def get_dalle2_image(prompt: str):
    headers = {
        "Authorization": "Bearer xxxxx",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "image-alpha-001",
        "num_images": 1,
        "size": 512*742,
        "response_format": "url"
    }
    response = requests.post("https://api.openai.com/v1/images/generations/dall-e/2", headers=headers, json=data)
    if response.status_code == 200:
        return {"image_url": response.json()["data"][0]["url"]}
    else:
        return {"error": "Failed to get DALL-E 2 image."}

def add_text(history, text):
    history = history + [(text, None)]
    return history, ""

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def gpt3_bot(history):
    print("bot history1===",history)
    prompt = history[-1][0]
    print(prompt)
    response = get_gpt3_results(prompt)
    history[-1][1] = response
    print("bot history2===",history)
    return history

def dalle2_bot(history):
    print("bot history1===",history)
    prompt = history[-1][0][0]
    print(prompt)
    response = get_dalle2_image(prompt)
    history[-1][1] = response
    print("bot history2===",history)
    return history

# def bot(history):
#     print("bot history1===",history)
#     response = "**That's cool!**"
#     history[-1][1] = response
#     print("bot history2===",history)
#     return history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot([], elem_id="chatbot").style(height=750)

    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
            txt.select(lambda x: "Hello, " + x + " demo1 !")
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
        gpt3_bot, chatbot, chatbot
    )

    txt_btn = gr.Button(value="Submit")
    txt_btn.click(add_text, [chatbot, txt], [chatbot, txt]).then(
        gpt3_bot, chatbot, chatbot
    )

    btn.upload(add_file, [chatbot, btn], [chatbot]).then(
        dalle2_bot, chatbot, chatbot
    )

if __name__ == "__main__":
  demo.launch(share=True)
  uvicorn.run(app='2_get:app', host="127.0.0.1", port=9806,reload=True, debug=True)