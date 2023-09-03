from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import datetime
import pytz
from openpyxl import Workbook
import langid
import sys



#create a browser class for the selenium
class Browser:

    def __init__(self):
        
        self.delay = 1 #wait 1 sec for page load

        chrome_options = Options()
        # chrome_options.add_argument("--headless")


        path = './chrome_driver/chromedriver' #specify path to the chrome driver.
        service = Service(path)


        # Create a Chrome browser using the Service object
        self.browser = webdriver.Chrome(service=service, options = chrome_options)
        self.browser.maximize_window()

# class for exporting mentions to xls        

class MentionsExporter:
    def __init__(self, mentions):
        self.mentions = mentions
        self.wb = Workbook()
        self.ws = self.wb.active
        self.write_header()

    def write_header(self):
        self.ws.append(['Date','Quarter', 'Source', 'Market', 'Type', 'Headline', 'Sentiment', 'Category', 'Channel', 'Language', 'Audience', 'Publicity'])

    def write_mentions(self):
        for i, mention in enumerate(self.mentions):
            self.ws.append([mention._date, mention.quarter, mention._source, mention._market, mention._type, mention._headline, mention._sentiment, mention._category, mention._channel, mention.lang, mention.audience, mention.publicity])

    def export_to_excel(self, filename):
        self.write_mentions()
        self.wb.save(filename)





#create the scraper class. This class inherits from the browser class
class Scraper(Browser):

    def __init__(self,url):
        super().__init__()
        self.url = url
        self.all_mentions = []
        self.counter = 0
        self.total_mentions = 0
        self.page_num = 0
        self.browser.get(self.url)
        time.sleep(self.delay * 5)
        # briana.lion@publicissapient.com
        # monitorTV3


    def login(self):
        # user = input("Enter username:")
        # password = input("Enter password:")
        login = self.browser.find_element(By.CSS_SELECTOR,value="#menu-item-3589 > a:nth-child(1)")
        login.click()
        time.sleep(self.delay * 3)
        try:
            self.browser.find_element(By.CSS_SELECTOR,value="#username").send_keys('briana.lion@publicissapient.com')
            self.browser.find_element(By.CSS_SELECTOR,value="#password").send_keys('monitorTV3')
            self.browser.find_element(By.CSS_SELECTOR,value="#password").send_keys(Keys.ENTER)
            time.sleep(self.delay * 20)
        except:
            print("Login invalid. Check credentials and try again...")

    def get_mentions(self):
        self.browser.find_element(By.CSS_SELECTOR,value=".nav-bar__links > a:nth-child(2)").click() #click the mentions tab
        time.sleep(self.delay)

        #choose the date range to filter
        while True:
            proceed = input("Select date range manually. Type 'done' to proceed: ")
            if 'done' in proceed.lower():
                break
            else:
                continue

        self.select_search_keywords() #add filter keywords

        self.total_mentions = float(self.browser.find_element(By.CSS_SELECTOR,value=".total").text.split()[0].replace(",","")) # get total mentions
        print(f"There {self.total_mentions} mentions available ")

        time.sleep(self.delay * 3)

        self.show_max_mentions() # show 500 mentions    

        # self.select_start_page() # uncomment this and specify the page you want to start again in the console. this is useful when scraper is interrupted you don't want to start again from page 1. make sure to backup the output first or it will get overwritten

        # start pagination loop
        try:
            self.get_page_mentions()
            while(self.is_next_page_available()):
                # try:
                self.browser.find_element(By.CSS_SELECTOR,value="#main_panel > div > div.results-navigation > div.results > div > div > div > div > div:nth-child(3) > div > button.btn-next").click()
                time.sleep(self.delay * 20)
                self.get_page_mentions()
                    # continue
                # except:
                #     print("Pagination exhausted.")
                #     break
            print('Pagination exhausted.')
        except:
            print("Job interrupted. Exporting all mentions")
            self.export_all_mentions()


    
    def select_date_range(self):
        start = input("Enter start date - mm/dd/yyyy hh:mm am|pm: ")
        end = input("Enter end date - mm/dd/yyyy hh:mm: am|pm: ")
        #01/01/2022 12:00 AM
        self.browser.find_element(By.CSS_SELECTOR,value="input.date-select:nth-child(2)").clear()
        time.sleep(self.delay)
        self.browser.find_element(By.CSS_SELECTOR,value="input.date-select:nth-child(2)").send_keys(start)
        self.browser.find_element(By.CSS_SELECTOR,value="body").click() # remove pop up calendar to locate proper css selector for end date by clicking body
        time.sleep(self.delay) #wait for calendar to load
        self.browser.find_element(By.CSS_SELECTOR,value="input.date-select:nth-child(2)").send_keys(Keys.TAB)

        self.browser.find_element(By.CSS_SELECTOR,value="input.date-select:nth-child(5)").clear()
        time.sleep(self.delay) #wait for calendar to load
        self.browser.find_element(By.CSS_SELECTOR,value="input.date-select:nth-child(5)").send_keys(end)
        time.sleep(self.delay) #wait for calendar to load
        self.browser.find_element(By.CSS_SELECTOR,value="input.date-select:nth-child(5)").send_keys(Keys.TAB)

        time.sleep(self.delay * 3)

    def show_max_mentions(self):
        self.browser.find_element(By.CSS_SELECTOR,value="#s2id_autogen3").click()
        time.sleep(1)
        self.browser.find_element(By.CSS_SELECTOR,value="li.select2-results-dept-0:nth-child(5)").click()
        time.sleep(self.delay * 10)

    def select_start_page(self):
        start = input("Enter start page: ")
        self.page_num = start
        self.jump_to_page(start)

    def jump_to_page(self,page):
        url = self.browser.current_url
        print(f"Current url {url}")
        if 'page=1' in url:
            url = url.replace('page=1','page='+str(page))
            self.page_num = int(self.page_num) + 1
        else:
            raise Exception("That page is not available to be changed.")
        self.browser.get(url)
        time.sleep(self.delay)
        self.browser.refresh()
        time.sleep(self.delay * 20)

    def get_page_mentions(self):
        elements = self.browser.find_elements(By.CSS_SELECTOR,value="div.search-result-mention__container > div:nth-child(2) > div")
        # elements = self.browser.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div")
        print(f"{len(elements)} mentions detected in this page")
        for key,elem in enumerate(elements):
            mention = Mention(self.browser,elem)
            print(f'Page mention number - {key}')
            print(mention)
            self.all_mentions.append(mention)
    
    def is_next_page_available(self):
        print("Click attempt to next page.")
        try:
            # self.browser.find_element(By.CSS_SELECTOR,value="div.search-result-mention-nav > div:nth-child(1) > button:nth-child(3)").click()
            self.browser.find_element(By.CSS_SELECTOR,value="#main_panel > div > div.results-navigation > div.results > div > div > div > div > div:nth-child(3) > div > button.btn-next[disabled=disabled]")
            print('Pagination exhausted.')
            return False
        except:
            return True
    
    def select_search_keywords(self):
        search_list = self.browser.find_elements(By.CSS_SELECTOR,value=".facet-values > li")
        for l in search_list:
            if 'PS DBT Sudheer - Brand Scorecard' in l.text:
                l.click()
                print("Search term selected.")
                time.sleep(self.delay * 5)

    def export_all_mentions(self):
        print("Exporting all mentions.")
        mentions_exporter = MentionsExporter(self.all_mentions)
        mentions_exporter.export_to_excel('CriticalMentions_Data_.xls')



class Mention:
    def __init__(self, browser, elem):
        self.browser = browser
        self.elem = elem

        # date and quarter
        date_text = self.elem.find_element(By.CSS_SELECTOR,value="div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)").text
        
        # Create a datetime object from the given date-time string
        if 'EDT' in date_text:
            date_time_str = date_text.replace('EDT', '-0400')
            date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d, %Y %I:%M %p %z')

            # Define the timezone object for Central Time (CT)
            ct_tz = pytz.timezone('US/Central')

            # Convert the datetime object to Central Time (CT)
            ct_datetime = date_time_obj.astimezone(ct_tz)

            self._date = ct_datetime.strftime('%b %d, %Y %I:%M %p %Z')
            
            # quarter
            quarter_dict = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2', 7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
            self._quarter = quarter_dict[(ct_datetime.month-1)//3 + 1]
        
        elif 'EST' in date_text:
            date_time_str = date_text.replace('EST', '-0500')
            date_time_obj = datetime.datetime.strptime(date_time_str, '%b %d, %Y %I:%M %p %z')

            # Define the timezone object for Central Time (CT)
            ct_tz = pytz.timezone('US/Central')

            # Convert the datetime object to Central Time (CT)
            ct_datetime = date_time_obj.astimezone(ct_tz)

            self._date = ct_datetime.strftime('%b %d, %Y %I:%M %p %Z')
            
            # quarter
            quarter_dict = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2', 7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
            self._quarter = quarter_dict[(ct_datetime.month-1)//3 + 1]
        else:
            self._date = date_text
            
            #quarter
            quarter_dict = {1: 'Q1', 2: 'Q1', 3: 'Q1', 4: 'Q2', 5: 'Q2', 6: 'Q2', 7: 'Q3', 8: 'Q3', 9: 'Q3', 10: 'Q4', 11: 'Q4', 12: 'Q4'}
            date_obj = datetime.datetime.strptime(date_text, '%b %d, %Y %I:%M %p %Z')
            self._quarter = quarter_dict[(date_obj.month-1)//3 + 1]


        self.expand_mention()
        # source
        try:
            # source_text = [x.text for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'source' in x.text.lower()]
            source_text = [x.text for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'source' in x.text.lower()]
            if source_text:
                self.source = ' '.join(source_text[0].split()).replace('Source','').strip()
            else:
                self.source = "N/A"
        except (NoSuchElementException, IndexError):
            self.source = "N/A"
        
        # market
        try:
            # labels_elem = self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") # get labels to check if 'market' word present
            labels_elem = self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") # get labels to check if 'market' word present
            # print(f'Labels: {len(labels_elem)}')
            market_text = ''
            for key,e in enumerate(labels_elem):
                # print(f'current label: {e.text}')
                if 'market' in e.find_element(By.CSS_SELECTOR,'span:nth-child(1)').text.lower():
                    # market_text = self.elem.find_elements(By.CSS_SELECTOR,value="#main_panel > div > div.results-navigation > div.results > div > div > div > div > div:nth-child(2) > div > div.mention-metadata--wrapper.search-result-mention > div > div.expanded-mention__container > div.expanded-mention__media-wall > div.mention-metadata__wall.font-size--12 > div > div")[key].text
                    market_text = e.find_element(By.CSS_SELECTOR,value="span:nth-child(2)").text
            if market_text:
                self.market = ' '.join(market_text.split()).strip()
            else:
                self.market = "N/A"
        except (NoSuchElementException, IndexError):
            self.market = "N/A"
        
        # type
        try:
            # type_text = [x.text for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'type' in x.text.lower()]
            type_text = [x.text for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'type' in x.text.lower()]
            if type_text:
                self.type = type_text[0].replace('Type','').strip()
            else:
                self.type = "N/A"
        except (NoSuchElementException, IndexError):
            self.type = "N/A"
        
        # headline
        self._headline = self.elem.find_element(By.CSS_SELECTOR,value="div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(2) > span:nth-child(1)").text
        
        # setinement
        try:
            self._sentiment = self.elem.find_element(By.CSS_SELECTOR,value="div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)").text
        except NoSuchElementException:
            self._sentiment = "N/A"
        
        # category
        try:
            # category_text = [x.text for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'category' in x.text.lower()]
            category_text = [x.text for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'category' in x.text.lower()]
            if category_text:
                self.category = ' '.join(category_text[0].replace('Category','').split()).strip()
            else:self.category = "N/A"
        except (NoSuchElementException, IndexError):
            self.category = "N/A"
        
        # channel
        try:
            self._channel = self.elem.find_element(By.CSS_SELECTOR,value="div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1)").get_attribute("class").replace("mention-icon","").replace("-icon","").capitalize().strip()
        except NoSuchElementException:
            self._channel = self.elem.find_element(By.CSS_SELECTOR,value=".results > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > svg:nth-child(1)").get_attribute("class").split()[-1].replace("-icon","").capitalize().strip()
        
        # language
        try:
            # lang_text = [x.text.replace('"','') for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'language' in x.text.lower()]
            lang_text = [x.text.replace('"','') for x in self.elem.find_elements(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div") if 'language' in x.text.lower()]
            if lang_text:
                self._lang = ' '.join(lang_text[0].split()).replace('Language','').strip()
            else:
                self._lang = "N/A"
        except (NoSuchElementException, IndexError):
            self._lang = "N/A"

        # audience
        try:
            audience_text = [x.text for x in self.elem.find_elements(By.CSS_SELECTOR,value="div.mention-metadata__column > div:nth-child(1)") if 'audience' in x.text.lower()]
            if audience_text:
                self._audience = ' '.join(audience_text[0].split()).replace("Audience","").strip()
            else:
                self._audience = "N/A"
        except (NoSuchElementException, IndexError):
            self._audience = "N/A"

        if 'N/A' not in self._audience:
            if 'k' in self._audience.lower():
                self._audience = float(self._audience.lower().strip("k")) * 1000
            elif 'm' in self._audience.lower():
                self._audience = float(self._audience.lower().strip('m')) * 1000000
            else:
                pass
        
        # publicity
        try:
            self.publicity = [x.text for x in self.elem.find_elements(By.CSS_SELECTOR,value="div.mention-metadata__column > div") if 'publicity' in x.text.lower()]
            if self.publicity:
                self.publicity = ' '.join(self.publicity[0].split()).replace("Publicity","").strip()
            else:
                self.publicity = 'N/A'
        except (NoSuchElementException,IndexError) as e:
            self.publicity = "N/A"

        self.expand_mention()
        # time.sleep(10)
    
    def get_language_name(self, code):
        lang_dict = {
            'am': 'Amharic',
            'ar': 'Arabic',
            'bg': 'Bulgarian',
            'cs': 'Czech',
            'da': 'Danish',
            'de': 'German',
            'el': 'Greek',
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'hr': 'Croatian',
            'hu': 'Hungarian',
            'it': 'Italian',
            'ja': 'Japanese',
            'ka': 'Georgian',
            'ko': 'Korean',
            'la': 'Latin',
            'nl': 'Dutch',
            'pl': 'Polish',
            'pt': 'Portuguese',
            'ro': 'Romanian',
            'ru': 'Russian',
            'sv': 'Swedish',
            'tl': 'Tagalog',
            'tr': 'Turkish',
            'vi': 'Vietnamese',
            'zh': 'Chinese'
        }
        return lang_dict.get(code, 'Unknown')

    def expand_mention(self):
        while True:
            # print("Expanding mention.")
            try:
                # self.elem.find_element(By.CSS_SELECTOR,value="div.search-result-mention__container > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)").click() #expand mention to reveal data on audience and publicity
                # self.elem.find_element(By.XPATH,value="/html/body/div[2]/div[2]/div[1]/div[2]/div/div[4]/div[2]/div/div/div/div/div[2]/div").click() #expand mention to reveal data on audience and publicity
                self.elem.click()
                time.sleep(0.6)
                break
            except:
                # ActionChains(self.browser).move_to_element(self.elem).perform()
                self.browser.execute_script("arguments[0].scrollIntoView();", self.elem) #scroll into view
                time.sleep(1)
                continue
    
    def __str__(self):
        return ("Mention:\n"
            "  Date:{}\n"
            "  Quarter:{}\n"
            "  Source:{}\n"
            "  Market:{}\n"
            "  Type:{}\n"
            "  Headline:{}\n"
            "  Sentiment:{}\n"
            "  Category:{}\n"
            "  Channel:{}\n"
            "  Lang:{}\n"
            "  Audience:{}\n"
            "  Publicity:{}\n"
            ).format(self.date, self.quarter, self.source, self.market, 
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

    # Getter and setter for date attribute
    @property
    def quarter(self):
        return self._quarter
    
    @quarter.setter
    def quarter(self, value):
        self._quarter = value

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
    # @property
    # def confidence(self):
    #     return self._confidence
    
    # @confidence.setter
    # def confidence(self,value):
    #     self._confidence = value


    # Getter and setter for audience attribute
    @property
    def audience(self):
        return self._audience
    
    @audience.setter
    def audience(self,value):
        self._audience = value

    # Getter and setter for publicity attribute
    @property
    def publicity(self):
        return self._publicity
    
    @publicity.setter
    def publicity(self,value):
        self._publicity = value








if __name__ == '__main__':
    url = "https://www.criticalmention.com/"
    scraper = Scraper(url)
    scraper.login()
    scraper.get_mentions()
    scraper.export_all_mentions()