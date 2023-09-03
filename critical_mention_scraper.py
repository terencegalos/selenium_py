from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from textblob import TextBlob
import langid
import xlwt
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



#create a browser class for the selenium
class Browser:

    def __init__(self):
        path = './firefox_driver/geckodriver' #specify path to the firefox driver.
        self.delay = 1 #wait 1 sec for page load
        self.browser = webdriver.Firefox(executable_path = path)
        self.browser.maximize_window()

# class for exporting mentions to xls        
class MentionsExporter:
    def __init__(self, mentions):
        self.mentions = mentions
        self.wb = xlwt.Workbook()
        self.ws = self.wb.add_sheet('Mentions')
        self.write_header()

    def write_header(self):
        self.ws.write(0, 0, 'Date')
        self.ws.write(0, 1, 'Source')
        self.ws.write(0, 2, 'Market')
        self.ws.write(0, 3, 'Type')
        self.ws.write(0, 4, 'Headline')
        self.ws.write(0, 5, 'Sentiment')
        self.ws.write(0, 6, 'Category')
        self.ws.write(0, 7, 'Channel')
        self.ws.write(0, 8, 'Language')
        self.ws.write(0, 9, 'Confidence')
        self.ws.write(0, 10, 'Audience')
        self.ws.write(0, 11, 'Publicity')

    def write_mentions(self):
        for i, mention in enumerate(self.mentions):
            self.ws.write(i+1, 0, mention._date.decode('utf-8'))
            self.ws.write(i+1, 1, mention._source.decode('utf-8'))
            self.ws.write(i+1, 2, mention._market)
            self.ws.write(i+1, 3, mention._type)
            self.ws.write(i+1, 4, mention._headline)
            self.ws.write(i+1, 5, mention._sentiment)
            self.ws.write(i+1, 6, mention._category.decode('utf-8'))
            self.ws.write(i+1, 7, mention._channel.decode('utf-8'))
            self.ws.write(i+1, 8, mention.lang)
            self.ws.write(i+1, 9, mention.confidence)
            self.ws.write(i+1, 10, mention.audience)
            self.ws.write(i+1, 11, mention.publicity)

    def export_to_excel(self, filename):
        self.write_mentions()
        self.wb.save(filename)




#create the scraper class. This class inherits from the browser class
class Scraper(Browser):

    def __init__(self,url):
        Browser.__init__(self)
        self.url = url
        self.all_mentions = []
        self.counter = 0
        self.total_mentions = 0


    def login(self):
        self.browser.get(url)
        time.sleep(self.delay)
        user = raw_input("Enter username:")
        password = raw_input("Enter password:")
        self.browser.find_element_by_css_selector("#menu-item-3589 > a:nth-child(1)").click()
        time.sleep(self.delay * 3)
        try:
            self.browser.find_element_by_css_selector("#username").send_keys(user)
            self.browser.find_element_by_css_selector("#password").send_keys(password)
            self.browser.find_element_by_css_selector("#password").send_keys(Keys.ENTER)
            time.sleep(self.delay * 5)
        except:
            print("Login invalid. Check credentials and try again...")

    def get_mentions(self):
        self.browser.find_element_by_css_selector(".nav-bar__links > a:nth-child(2)").click() #click the mentions tab
        time.sleep(self.delay)

        #choose the date range to filter
        while True:
            proceed = raw_input("Select date range. Type 'done' to proceed: ")
            if 'done' in proceed.lower():
                break
            else:
                continue

        self.select_search_keywords() #add filter keywords

        self.total_mentions = float(self.browser.find_element_by_css_selector(".total").text.split()[0].replace(",","")) # get total mentions
        print("There %d pages available " %self.total_mentions)

        time.sleep(self.delay * 3)
        self.show_max_mentions() # show 500 mentions    

        self.select_start_page()
        try:
            self.get_page_mentions()
            while(self.is_next_page_available()):
                # if self.counter < 1:
                #     break
                try:
                    self.browser.find_element_by_css_selector("div.search-result-mention-nav > div:nth-child(1) > button:nth-child(3)").click()
                    time.sleep(self.delay * 5)
                    self.get_page_mentions()
                    # self.counter += 1
                    continue
                except:
                    print("Pagination exhausted.")
                    break
        except:
            print("Job interrupted. Exporting all mentions")
            self.export_all_mentions()
    
    def select_date_range(self):
        start = raw_input("Enter start date - mm/dd/yyyy hh:mm am|pm: ")
        end = raw_input("Enter end date - mm/dd/yyyy hh:mm: am|pm: ")
        #01/01/2022 12:00 AM
        self.browser.find_element_by_css_selector("input.date-select:nth-child(2)").clear()
        time.sleep(self.delay)
        self.browser.find_element_by_css_selector("input.date-select:nth-child(2)").send_keys(start)
        self.browser.find_element_by_css_selector("body").click() # remove pop up calendar to locate proper css selector for end date by clicking body
        time.sleep(self.delay) #wait for calendar to load
        self.browser.find_element_by_css_selector("input.date-select:nth-child(2)").send_keys(Keys.TAB)

        self.browser.find_element_by_css_selector("input.date-select:nth-child(5)").clear()
        time.sleep(self.delay) #wait for calendar to load
        self.browser.find_element_by_css_selector("input.date-select:nth-child(5)").send_keys(end)
        time.sleep(self.delay) #wait for calendar to load
        self.browser.find_element_by_css_selector("input.date-select:nth-child(5)").send_keys(Keys.TAB)

        time.sleep(self.delay * 3)

    def show_max_mentions(self):
        self.browser.find_element_by_css_selector("#s2id_autogen3").click()
        time.sleep(1)
        self.browser.find_element_by_css_selector("li.select2-results-dept-0:nth-child(5)").click()
        time.sleep(self.delay * 10)

    def select_start_page(self):
        start = raw_input("Enter start page: ")
        url = self.browser.current_url
        print("Current url %s" %url)
        if 'page=1' in url:
            url = url.replace('page=1','page='+str(start))
        else:
            raise "That page is not available to be changed."
        self.browser.get(url)
        time.sleep(self.delay)
        self.browser.refresh()
        time.sleep(self.delay * 5)

    def get_page_mentions(self):
        elements = self.browser.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div")
        print("%d mentions detected in this page" %len(elements))
        for elem in elements:
            mention = Mention(self.browser,elem)
            print mention
            self.all_mentions.append(mention)
    
    def is_next_page_available(self):
        print("Click attempt to next page.")
        try:
            self.browser.find_element_by_css_selector("div.search-result-mention-nav > div:nth-child(1) > button:nth-child(3)")
            return True
        except:
            return False
    
    def select_search_keywords(self):
        search_list = self.browser.find_elements_by_css_selector(".facet-values > li")
        for l in search_list:
            if 'PS DBT Sudheer - Brand Scorecard' in l.text:
                l.click()
                print("Search term selected.")
                time.sleep(self.delay)

    def export_all_mentions(self):
        print("Exporting all mentions.")
        mentions_exporter = MentionsExporter(self.all_mentions)
        mentions_exporter.export_to_excel('filtered_mentions_output.xls')

            


class Mention:
    def __init__(self, browser, elem):
        self.browser = browser
        self.elem = elem
        self._date = self.elem.find_element_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)").text.encode('utf-8')
        try:
            self._source = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div div") if 'source' in s.text.lower()][0].strip("Source ")
        except:
            src = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div") if 'source' in s.text.lower()]
            self._source = ' '.join(src)
        try:
            self._market = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div div") if 'market' in s.text.lower()][0].strip("Market ")
        except:
            self._market = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div") if 'market' in s.text.lower()]
            self.market = ' '.join(self._market)
        try :
            # type = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div div") if 'type' in s.text.lower()]
            type = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div") if 'type' in s.text.lower()]
            if type:
                self._type = type[0].strip("Type ")
            else:
                print("Type not detected.")
                self._type = "N/A"
        except NoSuchElementException:
            self._type = "N/A"
        self._headline = self.elem.find_element_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)").text
        try:
            self._sentiment = self.elem.find_element_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)").text
        except NoSuchElementException:
            self._sentiment = "N/A"
        try:
            # category_text = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div div") if 'category' in s.text.lower()]
            category_text = [s.text for s in self.elem.find_elements_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div") if 'category' in s.text.lower()]
            if category_text:
                self._category = category_text[0].strip("Category ")
            else:
                print("Category not detected.")
                self._category = "N/A"

        except NoSuchElementException:
            self._category = "N/A"
        self._channel = self.elem.find_element_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)").get_attribute("class").encode("utf-8").strip("mention-icon ")
        try:
            b = self.elem.find_element_by_css_selector("div.mention-text-block").text #detect language with TextBlob
        except NoSuchElementException:
            b = self.elem.find_element_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2)").text #detect language with TextBlob
        self.lang,self.confidence = langid.classify(b)
        self.expand_mention()
        try:
            audience_text = [x.text.encode('utf-8') for x in self.elem.find_elements_by_css_selector("div.font-size--16") if 'audience' in x.text.lower()]
            if audience_text:
                self.audience = audience_text[0].strip("Audience")
            else:
                self.audience = "N/A"
            self.audience = "{}".format(self.audience.decode('utf-8', 'ignore').encode('utf-8')).replace("Audience ","")
        except (NoSuchElementException, IndexError):
            self.audience = "N/A"
        try:
            self.publicity = [x.text.encode('utf-8') for x in self.elem.find_elements_by_css_selector("div.font-size--16") if 'publicity' in x.text.lower()]
            if self.publicity:
                self.publicity = self.publicity[0].strip("Publicity")
            else:
                self.publicity = 'N/A'
            self.publicity = self.publicity.encode('utf-8', 'ignore').decode('ascii', 'ignore').replace("Publicity ","")
        except (NoSuchElementException,IndexError) as e:
            self.publicity = "N/A"

        self.expand_mention()
    
    def expand_mention(self):
        while True:
            try:
                self.elem.find_element_by_css_selector("div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > svg:nth-child(1)").click() #expand mention to reveal data on audience and publicity
                time.sleep(0.5)
                break
            except:
                # ActionChains(self.browser).move_to_element(self.elem).perform()
                self.browser.execute_script("arguments[0].scrollIntoView();", self.elem) #scroll into view
                time.sleep(1)
                continue
    
    def __str__(self):
        return ("Mention:\n"
            "  Date: {}\n"
            "  Source: {}\n"
            "  Market: {}\n"
            "  Type: {}\n"
            "  Headline: {}\n"
            "  Sentiment: {}\n"
            "  Category: {}\n"
            "  Channel: {}\n"
            "  Lang: {}\n"
            "  Audience: {}\n"
            "  Publicity: {}\n"
            ).format(self.date, self.source, self.market, 
                     self.type, self.headline, self.sentiment, 
                     self.category, self.channel, self.lang,
                     self.audience,
                     self.publicity
                     )

    # Getter and setter for date attribute
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value

    # Getter and setter for source attribute
    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, value):
        self._source = value

    # Getter and setter for market attribute
    @property
    def market(self):
        return self._market
    
    @market.setter
    def market(self, value):
        self._market = value

    # Getter and setter for type attribute
    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value

    # Getter and setter for headline attribute
    @property
    def headline(self):
        return self._headline
    
    @headline.setter
    def headline(self, value):
        self._headline = value

    # Getter and setter for sentiment attribute
    @property
    def sentiment(self):
        return self._sentiment
    
    @sentiment.setter
    def sentiment(self, value):
        self._sentiment = value

    # Getter and setter for category attribute
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        self._category = value

    # Getter and setter for channel attribute
    @property
    def channel(self):
        return self._channel
    
    @channel.setter
    def channel(self, value):
        self._channel = value

    # Getter and setter for lang attribute
    @property
    def lang(self):
        return self._lang
    
    @lang.setter
    def lang(self, value):
        self._lang = value


    # Getter and setter for confidence attribute
    @property
    def confidence(self):
        return self._confidence
    
    @confidence.setter
    def confidence(self,value):
        self._confidence = value


    # Getter and setter for audience attribute
    @property
    def audience(self):
        return self._audience
    
    @audience.setter
    def audience(self,value):
        self._audience = value.encode("utf-8")

    # Getter and setter for publicity attribute
    @property
    def publicity(self):
        return self._publicity
    
    @publicity.setter
    def publicity(self,value):
        self._publicity = value.encode("utf-8")








if __name__ == '__main__':
    url = "https://www.criticalmention.com/"
    scraper = Scraper(url)
    scraper.login()
    scraper.get_mentions()
    scraper.export_all_mentions()