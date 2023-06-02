import os, sys
import gradio as gr


def get_video(source_image,driven_audio,preprocess_type,is_still_mode,enhancer):
    print('入参：',source_image,driven_audio,preprocess_type,is_still_mode,enhancer)
    return "chinese_poem2.mp4"

def sadtalker_demo():

    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image",value="00004-3073250110.png", source="upload", type="filepath").style(height=256,width=256)
 
                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('Upload or Generating from TTS'):
                        with gr.Column(variant='panel'):
                            driven_audio = gr.Audio(label="Input audio(.wav/.mp3)",value="chinese_poem2.wav", source="upload", type="filepath")
                    
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        with gr.Column(variant='panel'):
                            preprocess_type = gr.Radio(['crop','resize','full'], value='crop', label='preprocess', info="How to handle input image?")
                            is_still_mode = gr.Checkbox(label="w/ Still Mode (fewer hand motion, works with preprocess `full`)")
                            enhancer = gr.Checkbox(label="w/ GFPGAN as Face enhancer")
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')

                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4").style(width=256)

        submit.click(
                    fn=get_video, 
                    inputs=[source_image,
                            driven_audio,
                            preprocess_type,
                            is_still_mode,
                            enhancer], 
                    outputs=[gen_video],
                    api_name='sad_talker'
                    )

    return sadtalker_interface
 

if __name__ == "__main__":

    demo = sadtalker_demo()
    demo.queue(max_size=10)
    demo.launch(debug=True)