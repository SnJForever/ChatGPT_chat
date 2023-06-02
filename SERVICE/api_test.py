from fastapi import FastAPI
import requests
import gradio as gr
import uvicorn

app = FastAPI()
@app.get("/")
def read_main():
    return {"message": "This is your main app"}
io = gr.Interface(lambda x: "Hello, " + x + "!", "textbox", "textbox")
app = gr.mount_gradio_app(app, io, path="/gradio")
# Then run `uvicorn run:app` from the terminal and navigate to http://localhost:8000/gradio.

if __name__ == "__main__":
#   demo.launch()
  uvicorn.run(app='api_test:app', host="127.0.0.1", port=9806,reload=True)