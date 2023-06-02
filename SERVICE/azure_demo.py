import azure.cognitiveservices.speech as speechsdk

def do_html_audio_speak_azure(words_to_speak):

    html_audio = '<pre>no audio</pre>'

    speech_key=""
    service_region="westeurope"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Note: the voice setting will not overwrite the voice element in input SSML.
    speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

    # 设置输出的音频文件路径和文件名
    audio_config = speechsdk.audio.AudioOutputConfig(filename="./tempfile.mp3")

    text = words_to_speak

    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))

do_html_audio_speak_azure("你好呀，jerry")