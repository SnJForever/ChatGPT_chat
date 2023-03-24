import uvicorn
from fastapi import FastAPI
import gradio as gr

app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "This is your main app"}

demo1 = gr.Interface(lambda x: "Hello, " + x + " demo1 !", "textbox", "textbox")
demo2 = gr.Interface(lambda x: "Hello, " + x + " demo2 !", "textbox", "textbox")

app = gr.mount_gradio_app(app, demo1, path="/")
app = gr.mount_gradio_app(app, demo2, path="/gradio")
demo = gr.Parallel(demo1, demo2)


if __name__ == "__main__":
  demo.launch(share=False)
  uvicorn.run(app='2_get:app', host="127.0.0.1", port=8888,reload=True, debug=True)