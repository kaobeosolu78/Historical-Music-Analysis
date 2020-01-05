import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

def load_obj(datatype):
    with open("{}".format(datatype) + '.pkl', 'rb') as f:
        return pickle.load(f)

def get_charting_titles(depth = 1,y_range = 9):
    chromedriver = ("C:\\Users\\Kaobe\\PycharmProjects\\School\\venv\\Include\\chromedriver.exe")
    driver = webdriver.Chrome(chromedriver)
    top = {}
    for k in range(y_range):
        if k <= 9:
            k = "0"+str(k)
        driver.get("https://www.billboard.com/charts/year-end/20{}/hot-r-and-and-b-hip-hop-songs".format(k))
        musicsoup = bs4.BeautifulSoup(driver.page_source,"html.parser")
        for j in range(depth):
            top[(musicsoup.findAll("div",class_="ye-chart-item__title")[j].text).replace("\n","")] = []
        time.sleep(2)
    return top

def get_charting_lyrics(titles):
    chromedriver = ("C:\\Users\\Kaobe\\PycharmProjects\\School\\venv\\Include\\chromedriver.exe")
    driver = webdriver.Chrome(chromedriver)
    for val in list(titles.keys()):
        lyrics = ""
        driver.get("https://www.google.com")
        search = driver.find_element_by_name("q")
        search.send_keys(val+" genius")
        search.send_keys(Keys.RETURN)
        driver.find_element_by_xpath("//*[@id=\"rso\"]/div/div/div[1]/div/div/div[1]/a/h3").click()

        musicsoup = bs4.BeautifulSoup(driver.page_source,"html.parser")
        titles[val] = musicsoup.findAll("p")[0].text
        for rval in ["[","]","Verse","Chorus","Bridge","(",")",",","'","?","1","2","3","4","5","6","7"]:
            titles[val] = titles[val].replace(rval, "")
        for k in range(len(top["Un-Thinkable (I'm Ready)"])):
            if titles[val][k].isupper() and titles[val][k - 1] != " ":
                lyrics += " " + titles[val][k]
            else:
                lyrics += titles[val][k]
        titles[val] = lyrics

    return titles

def process_data(data):
    ps = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    for stock1 in list(data.keys()):
        data[stock1] = [[com for com in word_tokenize(comm) if com not in stop_words] for comm in data[stock1]]
    all_words = []
    # for stock2 in list(data.keys()):
    #      data[stock2] = [ps.stem(word) for word in data[stock2]]
    for stock3 in list(data.keys()):
         all_words += [w.lower() for wo in data[stock3] for w in wo]

    al_words = nltk.FreqDist(all_words)
    common = al_words.most_common(50)
    print(common)
    common = [com for com in common if len(com) < 3]
    all_words = [al for al in al_words if al not in common]
    temp = nltk.FreqDist(all_words)
    print(temp.most_common(50))

toop = get_charting_titles(depth = 3,y_range =5)
top = load_obj("lyrics")

pickle_out = open("lyrics.pkl", 'wb')
pickle.dump(get_charting_lyrics(toop), pickle_out, pickle.HIGHEST_PROTOCOL)
pickle_out.close()
top = load_obj("lyrics")
for t in list((top).keys()):
    top[t] = [top[t]]
process_data(top)
print("")
#get_charting_lyrics(top)
