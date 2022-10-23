from googlesearch import search

class GoogleBanglaTextSearch:

    def __init__(self, tld="co.in", lang='eng', num=1, stop=1, pause=2) -> None:
        self.tld = tld
        self.lang = lang
        self.num = num
        self.stop = stop
        self.pause= pause
    
    def checkPlagiarism(self, text):
        result = '';
        for j in search(text, self.tld, self.num, self.lang, self.stop, self.pause):
            result = j;

        return result;