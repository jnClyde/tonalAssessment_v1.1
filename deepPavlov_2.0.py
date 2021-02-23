from Scraper import Scraper
from Preprocessing import Preprocessing
import codecs

def preprocTest():
    text1 = 'Ты собрал только половину пазла. Картина маслом, социальный лифт в пирамиде Маслоу. Толпа многоголова, как Гидра и Цербер.'
    text2 = 'Но она не делает погоду, как гидрометцентр.Ты умнее намного, нафиг плебеи такому?'
    data1 = Preprocessing(text1)
    data2 = Preprocessing(text2)
    print(data1.sentenceTokenize())
    print()
    print(data1.wordTokenize())
    print()
    print(data1.deleteRepeatLetters('прииииивеееетт'))
    print()
    print(data1.deleteRepeatLetters('вообще'))
    print()
    print(data2.deleteRubbish())

def main():
    #Тестирование класса скрепинга/парсинга страницы в соц.сети Твиттер на специально подготовленной страницы @Glibbort
    #user = 'Gllibort'
    #twiScraper = Scraper(user)
    #twiScraper.startScraper()
    

    #Тестирование классов препроцессинга
    preprocTest()
#---------------------------------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
    main()

