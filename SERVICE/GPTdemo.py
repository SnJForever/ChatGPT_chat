import gradio as gr
import openai
import requests
import csv
import uuid


prompt_templates = {"Default ChatGPT": ""}

def get_empty_state():
    return {"total_tokens": 0, "messages": []}

def download_prompt_templates():
    url = "https://raw.githubusercontent.com/f/awesome-chatgpt-prompts/main/prompts.csv"
    try:
        response = requests.get(url)
        reader = csv.reader(response.text.splitlines())
        next(reader)  # skip the header row
        for row in reader:
            if len(row) >= 2:
                act = row[0].strip('"')
                prompt = row[1].strip('"')
                prompt_templates[act] = prompt

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading prompt templates: {e}")
        return

    choices = list(prompt_templates.keys())
    choices = choices[:1] + sorted(choices[1:])
    return gr.update(value=choices[0], choices=choices)

def on_token_change(user_token):
    openai.api_key = user_token

def on_type_change(type):
    print(type)

def on_prompt_template_change(prompt_template):
    if not isinstance(prompt_template, str): return
    return prompt_templates[prompt_template]

def submit_message(type_select,user_token, prompt, prompt_template, temperature, max_tokens, context_length, state):
    print(type_select)
    history = state['messages']

    if not prompt:
        return gr.update(value=''), [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)], f"Total tokens used: {state['total_tokens']}", state
    
    prompt_template = prompt_templates[prompt_template]

    system_prompt = []
    if prompt_template:
        system_prompt = [{ "role": "system", "content": prompt_template }]

    prompt_msg = { "role": "user", "content": prompt }

    if not type_select:
        history.append(prompt_msg)
        history.append({
            "role": "system",
            "content": "Error: Type is not set."
        })
        return '', [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)], f"Total tokens used: 0", state

    if not user_token:
        history.append(prompt_msg)
        history.append({
            "role": "system",
            "content": "Error: OpenAI API Key is not set."
        })
        return '', [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)], f"Total tokens used: 0", state
    
    try:
        if type_select=='TEXT':
            text_history = [x for x in history if x['role'] != 'image' ]
            print(text_history)
            completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=system_prompt + text_history[-context_length*2:] + [prompt_msg], temperature=temperature, max_tokens=max_tokens)
            print(prompt_msg,completion.choices[0].message.to_dict())
            history.append(prompt_msg)
            history.append(completion.choices[0].message.to_dict())

            state['total_tokens'] += completion['usage']['total_tokens']
        elif type_select=='IMAGE':
            response = openai.Image.create(
                    prompt=prompt,
                    n=1,
                    size="512x512"
                    )
            print("image result ",response)
            image_url = response['data'][0]['url']

            history.append({ "role": "image", "content": prompt })
            history.append({ "role": "image", "content": image_url })

            state['total_tokens'] += 0
            
    except Exception as e:
        history.append(prompt_msg)
        history.append({
            "role": "system",
            "content": f"Error: {e}"
        })

    total_tokens_used_msg = f"Total tokens used: {state['total_tokens']}"

    chat_messages = [(history[i]['content'], history[i+1]['content']) for i in range(0, len(history)-1, 2)]
    print(1,chat_messages)
    chat_messages=[]
    for i in range(0, len(history)-1, 2):
        print(history[i])
        if(history[i]['role'] == 'image'):
            picture_name = str(uuid.uuid1())+'.png'
            reponse = requests.get(history[i+1]['content'])
            with open('/home/user/app/'+picture_name,'wb') as f:
                f.write(reponse.content)
            
            image_his = {'name': '/home/user/app/'+picture_name, 'mime_type': 'image/png', 'alt_text': None, 'data': None, 'is_file': True}
            
            chat_messages.append((history[i]['content'],image_his))

        else:
            chat_messages.append((history[i]['content'], history[i+1]['content']))
    print(2,chat_messages)
    return '', chat_messages, total_tokens_used_msg, state

def clear_conversation():
    return gr.update(value=None, visible=True), None, "", get_empty_state()


css = """
      #col-container {max-width: 80%; margin-left: auto; margin-right: auto;}
      #chatbox {min-height: 400px;}
      #header {text-align: center;}
      #prompt_template_preview {padding: 1em; border-width: 1px; border-style: solid; border-color: #e0e0e0; border-radius: 4px;}
      #total_tokens_str {text-align: right; font-size: 0.8em; color: #666;}
      #label {font-size: 0.8em; padding: 0.5em; margin: 0;}
      .message { font-size: 1.2em; }
      """

with gr.Blocks(css=css) as demo:
    
    state = gr.State(get_empty_state())


    with gr.Column(elem_id="col-container"):
        gr.Markdown("""## OpenAI ChatGPT chat
                    Using the ofiicial API (gpt-3.5-turbo model)
                    """,
                    elem_id="header")

        with gr.Row():
            with gr.Column(scale=0.7):
                chatbot = gr.Chatbot(elem_id="chatbox")
                with gr.Row():
                    with gr.Column(scale=0.2, min_width=0):
                        type_select = gr.Dropdown(show_label=False, choices= ["TEXT", "IMAGE"],value="TEXT",interactive=True)
                    with gr.Column(scale=0.8):
                        input_message = gr.Textbox(show_label=False, placeholder="Enter text and press enter", visible=True).style(container=False)
                btn_submit = gr.Button("Submit")
                total_tokens_str = gr.Markdown(elem_id="total_tokens_str")
                btn_clear_conversation = gr.Button("🔃 Start New Conversation")
            with gr.Column(scale=0.3):
                gr.Markdown("Enter your OpenAI API Key. You can get one [here](https://platform.openai.com/account/api-keys).", elem_id="label")
                user_token = gr.Textbox(value='', placeholder="OpenAI API Key", type="password", show_label=False)
                prompt_template = gr.Dropdown(label="Set a custom insruction for the chatbot:", choices=list(prompt_templates.keys()))
                prompt_template_preview = gr.Markdown(elem_id="prompt_template_preview")
                with gr.Accordion("Advanced parameters", open=False):
                    temperature = gr.Slider(minimum=0, maximum=2.0, value=0.7, step=0.1, label="Temperature", info="Higher = more creative/chaotic")
                    max_tokens = gr.Slider(minimum=100, maximum=4096, value=1000, step=1, label="Max tokens per response")
                    context_length = gr.Slider(minimum=1, maximum=10, value=2, step=1, label="Context length", info="Number of previous messages to send to the chatbot. Be careful with high values, it can blow up the token budget quickly.")

    # gr.HTML('''<br><br><br><center>You can duplicate this Space to skip the queue:<a href="https://huggingface.co/spaces/anzorq/chatgpt-demo?duplicate=true"><img src="https://bit.ly/3gLdBN6" alt="Duplicate Space"></a><br>
    #         <p><img src="https://visitor-badge.glitch.me/badge?page_id=anzorq.chatgpt_api_demo_hf" alt="visitors"></p></center>''')

    type_select.change(on_type_change,inputs=[type_select], outputs=[])
    btn_submit.click(submit_message, [type_select,user_token, input_message, prompt_template, temperature, max_tokens, context_length, state], [input_message, chatbot, total_tokens_str, state])
    input_message.submit(submit_message, [type_select,user_token, input_message, prompt_template, temperature, max_tokens, context_length, state], [input_message, chatbot, total_tokens_str, state])
    btn_clear_conversation.click(clear_conversation, [], [input_message, chatbot, total_tokens_str, state])
    prompt_template.change(on_prompt_template_change, inputs=[prompt_template], outputs=[prompt_template_preview])
    user_token.change(on_token_change, inputs=[user_token], outputs=[])

    
    demo.load(download_prompt_templates, inputs=None, outputs=[prompt_template], queur=False)


demo.queue(concurrency_count=10)
demo.launch(
    # auth=("admin", "IBTGeE3NrPsrViDI"),
    height='800px')