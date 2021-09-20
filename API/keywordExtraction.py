import yake

class KeywordExtractor:
    def __init__(self):
        self.language = "en"
        self.max_ngram_size = 2
        self.deduplication_threshold = 0.9
        self.numOfKeywords = 5
        self. kw_extractor = yake.KeywordExtractor(lan=self.language, n=self.max_ngram_size, dedupLim=self.deduplication_threshold, top=self.numOfKeywords, features=None)

    def keywordExtraction(self,text):
        keywords = self.kw_extractor.extract_keywords(text)
        keyword_list = []
        for kw in keywords:
           keyword_list.append(kw[0])

        return keyword_list

