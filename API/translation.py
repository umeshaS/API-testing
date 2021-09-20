from googletrans import Translator
class SinToEngTranslator:
    def __init__(self):
        pass

    def sinToEngTranslation(self,sinText):
        translator = Translator()
        engText = translator.translate(sinText, dest="en")
        return engText.text
