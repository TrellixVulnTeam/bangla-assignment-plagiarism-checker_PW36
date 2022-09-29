from cgitb import text
import nltk as nl
import os
import sqlite3
import re

class PlagiarismChecker:
    bangla_stopwords = ["অতএব",
                        "অথচ",
                        "অথবা",
                        "অনুযায়ী",
                        "অনেক",
                        "অনেকে",
                        "অনেকেই",
                        "অন্তত",
                        "অন্য",
                        "অবধি",
                        "অবশ্য",
                        "অর্থাত",
                        "আই",
                        "আগামী",
                        "আগে",
                        "আগেই",
                        "আছে",
                        "আজ",
                        "আপনার",
                        "আপনি",
                        "আবার",
                        "আমরা",
                        "আমাকে",
                        "আমাদের",
                        "আমার",
                        "আমি",
                        "আর",
                        "আরও",
                        "ই",
                        "ইত্যাদি",
                        "ইহা",
                        "উচিত",
                        "উত্তর",
                        "উনি",
                        "উপর",
                        "উপরে",
                        "এ",
                        "এঁদের",
                        "এঁরা",
                        "এই",
                        "একই",
                        "একটি",
                        "একবার",
                        "একে",
                        "এক্",
                        "এখন",
                        "এখনও",
                        "এখানে",
                        "এখানেই",
                        "এটা",
                        "এটাই",
                        "এটি",
                        "এত",
                        "এতটাই",
                        "এতে",
                        "এদের",
                        "এব",
                        "এবং",
                        "এবার",
                        "এমন",
                        "এমনকী",
                        "এমনি",
                        "এর",
                        "এরা",
                        "এল",
                        "এস",
                        "এসে",
                        "ঐ",
                        "ও",
                        "ওঁদের",
                        "ওঁর",
                        "ওঁরা",
                        "ওই",
                        "ওকে",
                        "ওখানে",
                        "ওদের",
                        "ওর",
                        "ওরা",
                        "কখনও",
                        "কত",
                        "কবে",
                        "কমনে",
                        "কয়েক",
                        "কয়েকটি",
                        "করছে",
                        "করছেন",
                        "করতে",
                        "করবে",
                        "করবেন",
                        "করলে",
                        "করলেন",
                        "করা",
                        "করাই",
                        "করায়",
                        "করার",
                        "করি",
                        "করিতে",
                        "করিয়া",
                        "করিয়ে",
                        "করে",
                        "করেই",
                        "করেছিলে",
                        "করেছে",
                        "করেছেন",
                        "করেন",
                        "কাউকে",
                        "কাছ",
                        "কাছে",
                        "কাজ",
                        "কাজে",
                        "কারও",
                        "কারণ",
                        "কি",
                        "কিংবা",
                        "কিছু",
                        "কিছুই",
                        "কিন্তু",
                        "কী",
                        "কে",
                        "কেউ",
                        "কেউই",
                        "কেখা",
                        "কেন",
                        "কোটি",
                        "কোন",
                        "কোনও",
                        "কোনো",
                        "ক্ষেত্রে",
                        "কয়েক",
                        "খুব",
                        "গিয়ে",
                        "গিয়েছে",
                        "গিয়ে",
                        "গুলি",
                        "গেছে",
                        "গেল",
                        "গেলে",
                        "গোটা",
                        "চলে",
                        "চান",
                        "চায়",
                        "চার",
                        "চালু",
                        "চেয়ে",
                        "চেষ্টা",
                        "ছাড়া",
                        "ছাড়াও",
                        "ছিল",
                        "ছিলেন",
                        "জন",
                        "জনকে",
                        "জনের",
                        "জন্য",
                        "জানতে",
                        "জানা",
                        "জানানো",
                        "জানায়",
                        "জানিয়ে",
                        "জানিয়েছে",
                        "জে",
                        "জ্নজন",
                        "টি",
                        "ঠিক",
                        "তখন",
                        "তত",
                        "তথা",
                        "তবু",
                        "তবে",
                        "তা",
                        "তাঁকে",
                        "তাঁদের",
                        "তাঁর",
                        "তাঁরা",
                        "তাঁাহারা",
                        "তাই",
                        "তাও",
                        "তাকে",
                        "তাতে",
                        "তাদের",
                        "তার",
                        "তারপর",
                        "তারা",
                        "তারৈ",
                        "তাহলে",
                        "তাহা",
                        "তাহাতে",
                        "তাহার",
                        "তিনঐ",
                        "তিনি",
                        "তিনিও",
                        "তুমি",
                        "তুলে",
                        "তেমন",
                        "তো",
                        "তোমার",
                        "থাকবে",
                        "থাকবেন",
                        "থাকা",
                        "থাকায়",
                        "থাকে",
                        "থাকেন",
                        "থেকে",
                        "থেকেই",
                        "থেকেও",
                        "দিকে",
                        "দিতে",
                        "দিন",
                        "দিয়ে",
                        "দিয়েছে",
                        "দিয়েছেন",
                        "দিলেন",
                        "দু",
                        "দুই",
                        "দুটি",
                        "দুটো",
                        "দেওয়া",
                        "দেওয়ার",
                        "দেওয়া",
                        "দেখতে",
                        "দেখা",
                        "দেখে",
                        "দেন",
                        "দেয়",
                        "দ্বারা",
                        "ধরা",
                        "ধরে",
                        "ধামার",
                        "নতুন",
                        "নয়",
                        "না",
                        "নাই",
                        "নাকি",
                        "নাগাদ",
                        "নানা",
                        "নিজে",
                        "নিজেই",
                        "নিজেদের",
                        "নিজের",
                        "নিতে",
                        "নিয়ে",
                        "নিয়ে",
                        "নেই",
                        "নেওয়া",
                        "নেওয়ার",
                        "নেওয়া",
                        "নয়",
                        "পক্ষে",
                        "পর",
                        "পরে",
                        "পরেই",
                        "পরেও",
                        "পর্যন্",
                        "পাওয়া",
                        "পাচ",
                        "পারি",
                        "পারে",
                        "পারেন",
                        "পি",
                        "পেয়ে",
                        "পেয়্র্",
                        "প্রতি",
                        "প্রথম",
                        "প্রভৃতি",
                        "প্রাথমিক",
                        "প্রায়",
                        "প্রায়",
                        "ফলে",
                        "ফিরে",
                        "ফের",
                        "বদলে",
                        "বন",
                        "বরং",
                        "বলতে",
                        "বলল",
                        "বললেন",
                        "বলা",
                        "বলে",
                        "বলেছেন",
                        "বলেন",
                        "বসে",
                        "বহু",
                        "বা",
                        "বাদে",
                        "বার",
                        "বি",
                        "বিনা",
                        "বিভিন্ন",
                        "বিশেষ",
                        "বিষয়টি",
                        "বেশ",
                        "বেশি",
                        "ব্যবহার"
                        "ব্যাপারে",
                        "ভাবে",
                        "ভাবেই",
                        "মতো",
                        "মতোই",
                        "মধ্যভাগে"
                        "মধ্যে",
                        "মধ্যেই",
                        "মধ্যেও",
                        "মনে",
                        "মাত্র",
                        "মাধ্যমে",
                        "মোট",
                        "মোটেই",
                        "যখন",
                        "যত",
                        "যতটা",
                        "যথেষ্ট",
                        "যদি",
                        "যদিও",
                        "যা",
                        "যাঁর",
                        "যাঁরা",
                        "যাওয়া",
                        "যাওয়ার",
                        "যাওয়া",
                        "যাকে",
                        "যাচ্ছে",
                        "যাতে",
                        "যাদের",
                        "যান",
                        "যাবে",
                        "যায়",
                        "যার",
                        "যারা",
                        "যিনি",
                        "যে",
                        "যেখানে",
                        "যেতে",
                        "যেন",
                        "যেমন",
                        "র",
                        "রকম",
                        "রয়েছে",
                        "রাখা",
                        "রেখে",
                        "লক্ষ",
                        "শুধু",
                        "শুরু",
                        "সঙ্গে",
                        "সঙ্গেও",
                        "সব",
                        "সবার",
                        "সমস্ত",
                        "সম্প্রতি"
                        "সহ",
                        "সহিত",
                        "সাধারণ",
                        "সামনে",
                        "সি",
                        "সুতরাং",
                        "সে",
                        "সেই",
                        "সেখান",
                        "সেখানে",
                        "সেটা",
                        "সেটাই",
                        "সেটাও",
                        "সেটি",
                        "স্পষ্ট",
                        "স্বয়ং",
                        "হইতে",
                        "হইবে",
                        "হইয়া",
                        "হওয়া",
                        "হওয়ায়",
                        "হওয়ার",
                        "হচ্ছে",
                        "হত",
                        "হতে",
                        "হতেই",
                        "হন",
                        "হবে",
                        "হবেন",
                        "হয়",
                        "হয়তো",
                        "হয়নি",
                        "হয়ে",
                        "হয়েই",
                        "হয়েছিল",
                        "হয়েছে",
                        "হয়েছেন",
                        "হল",
                        "হলে",
                        "হলেই",
                        "হলেও",
                        "হলো",
                        "হাজার",
                        "হিসাবে",
                        "হৈলে",
                        "হোক",
                        "হয়"]

    # plagiarism detecting using nltk as same as sequence matcher
    def levenshtein(self, text1, text2):
        diff = nl.edit_distance(text1, text2)
        # FORMULA
        result = (1-(diff/max(len(text1), len(text2))))*100
        result = "{:.2f}".format(result)  # taking two decimal place value only

        return float(result)
    
    # checking every sentance where have similerities or not if then take in an array then the array will return
    def santenceSimilarity(self, text1, text2):
        similer_text = []
        for i in range(0,len(text1)):
            for j in range(0,len(text2)):
                if self.levenshtein(text1[i], text2[j]) > 70:
                    similer_text.append(text1[i])

        return similer_text     
    
    # every sentence summation the percentage
    def percentageOfText(self, text1, text2):
        sum = 0
        lenCount = 0
        for i in range(len(text1)):
            for j in range(len(text2)):
                per= self.levenshtein(text1[i], text2[j])
                if (per > 5):
                    sum += per
                    lenCount += 1
        return sum / lenCount
                    
    