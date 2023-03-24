from fastapi import FastAPI
import requests
import gradio as gr
import uvicorn


app = FastAPI()

@app.get("/gpt3")
def get_gpt3_results(prompt: str):
    print(prompt)
    headers = {
        "Authorization": "Bearer YOUR_GPT3_TOKEN",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "gpt3.5-turbo",
        "temperature": 0.5,
        "max_tokens": 100
    }
    response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["text"]
    else:
        return {"error": "Failed to get GPT-3.5-turbo results."}

@app.get("/dalle2")
def get_dalle2_image(prompt: str):
    headers = {
        "Authorization": "Bearer YOUR_DALLE2_TOKEN",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "model": "image-alpha-001",
        "num_images": 1,
        "size": 512,
        "response_format": "url"
    }
    response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=data)
    if response.status_code == 200:
        return {"image_url": response.json()["data"][0]["url"]}
    else:
        return {"error": "Failed to get DALL-E 2 image."}

greeter_1 = gr.Interface(get_gpt3_results, inputs=[gr.inputs.Textbox(label="Prompt")], outputs=gr.Textbox(label="Greeter 1"))
greeter_2 = gr.Interface(get_dalle2_image, inputs=[gr.inputs.Textbox(label="Prompt")], outputs=[gr.outputs.Image(label="Generated Image", type="filepath")])
demo = gr.Parallel(greeter_1, greeter_2)

while 1:
  demo.launch(share=False)
  uvicorn.run(app='2_get:app', host="127.0.0.1", port=8888,reload=True, debug=True)