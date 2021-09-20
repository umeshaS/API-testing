# -*- coding: utf-8 -*-
import re
from languageIdentificationInputPreprocessing import LanguageIdentificationPreprocessing
class ScriptIdentifier:
    def __init__(self):
        self.pre = LanguageIdentificationPreprocessing()

    def isEnglish(self,text):
        textPreprocessed = self.pre.remove_emails(text)
        textPreprocessed = self.pre.remove_url(textPreprocessed)
        textPreprocessed = self.pre.remove_punctuations(textPreprocessed)
        textPreprocessed = self.pre.remove_digits(textPreprocessed)
        textPreprocessed = self.pre.remove_extra_spaces(textPreprocessed)

        # try:
        #     textPreprocessed.encode(encoding='utf-8').decode('ascii')
        # except UnicodeDecodeError:
        #     return False
        # else:
        #     return True

        words = textPreprocessed.split()
        reg = re.compile(r'[a-zA-Z]')
        totalCount = len(words)
        print(totalCount)
        engCount = 0
        for word in words:
            if reg.match(str(word)):
                print("It is an alphabet")
                engCount += 1
            else:
                print("It is not an alphabet")
                print(word)
        print(engCount)

        if(engCount / totalCount) > 0.5:
            print('en')
            return 1
        else:
            return 0
