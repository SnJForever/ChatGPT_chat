from gradio_client import Client


import os
os.environ['NO_PROXY'] = 'https://b65c2e2e3e7c67e2df.gradio.live/'

# client = Client("SnJForever/ChatGPT-chat")  # connecting to a Hugging Face Space
# result = client.predict("SERVICE/00004-3073250110.png","SERVICE/chinese_poem2.wav","full",True,True, api_name="/sad_talker")
# print(result)



# client = Client("https://62ef160dc5539b9134.gradio.live/")  # connecting to a temporary Gradio share URL
# job = client.submit("SERVICE/00004-3073250110.png","SERVICE/chinese_poem2.wav","full",False,False, api_name="/sad_talker")  # runs the prediction in a background thread

# print(job.result())

import requests

import base64

GRADIO_URL = "https://d300ac5cd199aa843c.gradio.live"

def ToBase64(file):
    with open(file, 'rb') as fileObj:
        image_data = fileObj.read()
        base64_data = base64.b64encode(image_data)
        return base64_data.decode()
img_data = ToBase64("SERVICE/00004-3073250110.png")
audio_data = ToBase64("SERVICE/chinese_poem2.wav")

response = requests.post(GRADIO_URL+"/run/sad_talker", json={
	"data": [
		"data:image/png;base64,"+img_data,
		{"name":"audio.wav","data":"data:audio/wav;base64,"+audio_data},
	    "crop",
		False,
		False,
	]
},timeout=3000)
print(response.text)
res = response.json()

data = res["data"]
print(data)
video_rul = GRADIO_URL+"/file=" + data[0][0]['name']
print(video_rul)