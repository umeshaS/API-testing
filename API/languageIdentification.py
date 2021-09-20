import pickle
import numpy as np
from languageIdentificationInputPreprocessing import LanguageIdentificationPreprocessing
class LanguageIdentifier:
    def __init__(self):
        self.model = pickle.load(open('models/final_languageIdentification.pkl', 'rb'))
        self.vectorizer = pickle.load(open("models/vectorizer.pkl", 'rb'))
        self.pre = LanguageIdentificationPreprocessing()

    def languageIdentification(self, text):
        # removing emails
        x_input = self.pre.remove_emails(text)

        # removing URLs
        x_input = self.pre.remove_url(x_input)

        # remove special characters
        x_input = self.pre.remove_special_characters(x_input)

        # remove accented characters
        x_input = self.pre.remove_accented_chars(x_input)

        # remove extra spaces
        x_input = self.pre.remove_extra_spaces(x_input)

        # convert to lower case
        x_input = self.pre.convert_to_lowercase(x_input)

        word_list = x_input.split()


        # remove the same letter repeating for more than twice
        x_input = x_input.replace(x_input, self.pre.remove_consecutives(word_list))

        # vectorized using the pickled vectorizor
        x_inputting = self.vectorizer.transform([x_input])

        # predict the class labels using the pickled model
        prediction = np.array2string(self.model.predict(x_inputting))

        return prediction


