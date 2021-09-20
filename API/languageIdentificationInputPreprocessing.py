import re
import unicodedata
# from _cffi_backend import string
import string
# This function is to remove emails

class LanguageIdentificationPreprocessing:
    def __init__(self):
        pass
    def remove_emails(self,sample_string):
        """
        function to remove emails
        :param sample_string:str
        :rtype: str
        """
        output = re.sub(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', '', sample_string)
        return output


    def remove_url(self,sample_string):
        """
        function to remove urls
        :param sample_string:str
        :rtype: str
        """
        output = re.sub(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', '', sample_string)
        return output

    def remove_punctuations(self,sample_string):
        output = sample_string.translate(str.maketrans('', '', string.punctuation))
        return output

    def remove_digits(self,sample_string):
        output = re.sub(r'[0-9]', '', str(sample_string))
        return output

    def remove_special_characters(self,sample_string):
        """
        Function to remove special characters
        :param sample_string:str
        :return: str
        """
        output = re.sub('[^A-Z a-z 0-9-]+', '', sample_string)
        return output


    def convert_to_lowercase(self,sample_string):
        """
        Function to convert to lower case
        :param sample_string:str
        :return: str
        """
        output = sample_string.lower()
        return output


    def remove_extra_spaces(self,sample_string):
        """
        Function to remove extra spaces
        :param sample_string:str
        :return: str
        """
        output = " ".join(sample_string.split())
        return output


    def remove_consecutives(self,samplelist):
        """
        Function to convert to lower case
        :param samplelist:list
        :return: str
        """
        sentence = ""
        count = 1
        for j in range(len(samplelist)):
            word = samplelist[j]

            processedWord = word[0]

            for i in range(1, len(word)):
                if word[i] == word[i - 1]:
                    count = count + 1
                    if count <= 2:
                        processedWord = processedWord + word[i]

                else:
                    processedWord = processedWord + word[i]
                    count = 1

            sentence = sentence + " " + processedWord
        return sentence


    def remove_accented_chars(self,sample_string):
        """
        Function to accented chars
        :param sample_string:str
        :return: str
        """
        sample_string = unicodedata.normalize('NFKD', sample_string).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        return sample_string
