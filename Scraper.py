import os 
from time import sleep
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By 
from datetime import timedelta, datetime

from TwitterConst import _TwitterConst

class Scraper(_TwitterConst):
   
    def __init__(self, user):
        CONST = _TwitterConst()
        self._user = user
        self.__login = CONST.DEFAULT_LOGIN()
        self.__pass = CONST.DEFAULT_PASS()
        self.__path = CONST.DEFAULT_PATH()
        self.__checkDate = CONST.DEFAULT_CHECKDATE()
        self._authPage = CONST.DEFAULT_AUTHPAGE()

    def set_login(self, l):
        self.__login = l
    def set_pass(self, p):
        self.__pass = p
    def set_path(self, p):
        self.__path = p
    def set_checkDate(self, c):
        self.__checkDate = c
    def set_user(self, u):
        self._user = u

    def get_login(self):
        return self.__login
    def get_pass(self):
        return self.__pass
    def get_path(self):
        return self.__path
    def get_checkDate(self):
        return self.__checkDate
    def get_user(self):
        return self._user


    #Google chrome settings
    def driverSetting(self):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options) 
        driver.maximize_window()
        return driver

    #Authorization
    def logIn(self, driver):
            #login
            username = driver.find_element_by_xpath('//input[@name="session[username_or_email]"]')
            username.send_keys(self.__login)

            #password
            password = driver.find_element_by_xpath('//input[@name="session[password]"]')
            password.send_keys(self.__pass)
            password.send_keys(Keys.RETURN)

    def userPage(self, driver):
        userURL = 'http://www.twitter.com/' + self._user.lower()
        driver.get(userURL)

    #Collection data from user page
    def getPageData(self, driver):
        data = []
        tweet_ids = set()
        lastPosition = driver.execute_script("return window.pageYOffset;")
        scrolling = True
        first = True

        while scrolling:
            pageCards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')

            for card in pageCards[-15:]: #check only 15 latest tweets on page
                curDate = self.getDate(card)
                if (self.__checkDate > curDate):
                    scrolling = False
                    break
                tweet = self.getTweetData(card)
                #print(getDate(card))
                if tweet:
                    try: 
                        tweet_id = ''.join(tweet)
                        if tweet_id not in tweet_ids:
                            tweet_ids.add(tweet_id)
                            data.append(tweet)
                    except: 
                        continue
                        
            scrollAttempt = 0
            while True:
                # check scroll position
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                sleep(2)
                currPosition = driver.execute_script("return window.pageYOffset;")
                if lastPosition == currPosition:
                    scrollAttempt += 1
            
                    # end of scrolling
                    if scrollAttempt >= 3:
                        scrolling = False
                        break
                    else:
                        sleep(2) # attempt another scroll
                else:
                    lastPosition = currPosition
                    break
        return data

    #Check date of tweet
    def getDate(self, card):
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except:
            return datetime.now()
        date = postdate[0:10]
        year = date[:4]
        month = date[5:7]
        day = date[8:]
        curDate = datetime(int(year), int(month), int(day))
        return curDate

    #Get only text information of tweet
    def getTweetData(self, card):
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        text = comment + responding
        return text

    #Get full information(text, likes, retweets and comments)
    def getFullTweetData(self, card):
        username = card.find_element_by_xpath('.//span').text
        handle = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
        try:
            postdate = card.find_element_by_xpath('.//time').get_attribute('datetime')
        except NoSuchElementException:
            return
    
        comment = card.find_element_by_xpath('.//div[2]/div[2]/div[1]').text
        responding = card.find_element_by_xpath('.//div[2]/div[2]/div[2]').text
        text = comment + responding

        replyCount = self.getReplyCnt(card)
        retweetCount = self.getRetweetCnt(card)
        likeCount = self.getLikeCnt(card)

        tweet = (username, handle, postdate, text, replyCount, retweetCount, likeCount)
        return tweet

    #Methods that return number of likes/retweets(replyes)/comments
    def getReplyCnt(self, card):
        try:
            replyCount = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
        except: 
            replyCount = 0
        return replyreplyCount

    def getRetweetCnt(self, card):
        try: 
            retweetCount = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text
        except: 
            retweetCount = 0
        return retweetCount

    def getLikeCnt(self, card):
        try: 
            likeCount = card.find_element_by_xpath('.//div[@data-testid="like"]').text
        except:
            likeCount = 0
        return likeCount

    #Write data to txt file
    def writeTxt(self, data):
        with open(self.__path, 'w') as file:
            for item in data:
                try:
                    file.write("%s\n" % str(item))
                except:
                    continue

    def startScraper(self):
        #1 - start driver(Google Chrome)
        driver = self.driverSetting()
        #2 - go to auth page
        CONST = _TwitterConst()
        driver.get(CONST.DEFAULT_AUTHPAGE())
        #3 - login on page for Scraper
        self.logIn(driver)
        #4 - go to user page
        self.userPage(driver)
        #5 - getting data up to a certain date
        data = self.getPageData(driver)
        #6 - close data
        driver.close()
        #7 - write data in result.txt
        self.writeTxt(data)