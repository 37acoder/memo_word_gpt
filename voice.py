from gtts import gTTS
import io


def text_to_speech(text):
    tts = gTTS(text=text, lang='en')  # 将'lang'参数更改为所需的语言代码
    stream = io.BytesIO()
    tts.write_to_fp(stream)
    return stream.getvalue()

# # 示例用法
# text = "Hello, how are you?"
# filename = "output.mp3"
# text_to_speech(text, filename)