import pickle
from flask import Flask, request, jsonify
import translation as tr
from keywordExtraction import KeywordExtractor
from languageIdentification import LanguageIdentifier
from transliteration import Transliterator
from ScriptIdentification import ScriptIdentifier
app = Flask(__name__)

transliterator = Transliterator()
keywordExtractor = KeywordExtractor()
languageIdentifier = LanguageIdentifier()
translator = tr.SinToEngTranslator()
scriptidentifier = ScriptIdentifier()

# route for the language classification
@app.route('/languageIdentification', methods=["POST"])
# This function is to preprocess the input and predict and return the output of language identification
#
# returns json object
def classification():

    keywords = []
    input_sample = request.json["text"]
    outputTranslator = input_sample
    trans_text = input_sample
    isEnglish = scriptidentifier.isEnglish(input_sample)

    if isEnglish == 1:
        pred_romanized_lan = languageIdentifier.languageIdentification(input_sample)
        print("engisl")
        print(pred_romanized_lan)
        if (pred_romanized_lan == "[1]"):
            trans_text = transliterator.singlish2sinhala(input_sample)
            outputTranslator = translator.sinToEngTranslation(trans_text)
            keywords = keywordExtractor.keywordExtraction(outputTranslator)
        else:
            outputTranslator = translator.sinToEngTranslation(trans_text)
            keywords = keywordExtractor.keywordExtraction(outputTranslator)
    else:
        outputTranslator = translator.sinToEngTranslation(trans_text)
        keywords = keywordExtractor.keywordExtraction(outputTranslator)


    return jsonify(keywords,outputTranslator,trans_text,isEnglish)


if __name__ == '__main__':
    app.run()
