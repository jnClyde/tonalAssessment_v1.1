import nltk
import string
import pymorphy2
import sys
import locale
import itertools
import enchant

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from pymystem3 import Mystem
from string import punctuation
from hunspell import Hunspell

#---------------------------------------------------------------------------------------------------------------------------------------------#
# *Лемматиза́ция — процесс приведения словоформы к лемме — её нормальной (словарной) форме.(кошки -> кошка, бежал -> бежать)
# **Сте́мминг (англ. stemming — находить происхождение) — это процесс нахождения основы слова для заданного исходного слова.(ведущая -> ведущ)
#---------------------------------------------------------------------------------------------------------------------------------------------#

class Preprocessing:
    
    def __init__(self, data):
        self._data = data
        self._punctuation = string.punctuation
        self._stopWordsRU = stopwords.words("russian")
        self.mystem = Mystem()

    #проверка на правильность написания слова, то есть наличие его в словаре рус.яз.(# 'привет' -> true; 'прювет' -> false)
    def checkEnchant(self, word):
        dictionary = enchant.Dict("ru_RU")
        if dictionary.check(word): 
            return True
        else: return False

    #токенизация по предложениям
    def sentenceTokenize(self):
        return sent_tokenize(self._data, language="russian")

    #токенизация по словам
    def wordTokenize(self):
        return word_tokenize(self._data, language="russian")

    #лемматизация* при помощи стемминга
    def lemmatize(self):
        return self.mystem.lemmatize(self._data.lower())

    #удаление потворяющихся букв в слове(# 'прииииивеееееттт' -> 'привет')
    #предполагется использование, если слово не встречается в словаре
    # 'прииииивеееееттт' -> 'привет'; 'вообще' -> 'вообще'
    def deleteRepeatLetters(self, word):
        if (not(self.checkEnchant(word))): 
            return ''.join(ch for ch, _ in itertools.groupby(word))
        else: 
            return word

    #удаление из предложения стоп-слов, знаков препинания
    def deleteRubbish(self):
        tokens = self.lemmatize()
        tokens = [token for token in tokens if token not in self._stopWordsRU\
                  and token != " " \
                  and token.strip() not in punctuation]
    
        clearData = " ".join(tokens)
        return clearData

   






  

  



   
