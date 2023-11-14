from translate import Translator

translator = Translator(to_lang="zh", from_lang="en")

def translate_en_to_zh(text):
    translation = translator.translate(text)
    return translation
