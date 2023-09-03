from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import time
import pandas as pd
import logging

logging.basicConfig(filename='scraper.log',level=logging.ERROR,format='%(asctime)s %(levelname)s %(message)s')

class Browser:

    def __init__(self):
        
        path = '/chrome_driver/chromedriver'
        chrome_options = Options()
        service = Service(path)
        # chrome_options.add_argument('--headless')
        headless_mode = True
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        if headless_mode:
            chrome_options.add_argument(f'user-agent={user_agent}')
            chrome_options.add_argument('--log-level=3') # only display fatal errors
        chrome_options.add_argument('--window-size=1920,924') # set viewport size


        self.browser = webdriver.Chrome()#service=service,options=chrome_options)
        # print(self.browser.execute_script('return navigator.userAgent;'))
            
        self.browser.maximize_window()
        viewport_width = self.browser.execute_script('return Math.max(document.documentElement.clientWidth, window.innerWidth || 0);')
        viewport_height = self.browser.execute_script('return Math.max(document.documentElement.clientHeight,window.innerHeight || 0);')
        print('Width',viewport_width)
        print('Height',viewport_height)

class Review:

    def __init__(self,e,country):
        # rate
        rate_elem = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)')
        if rate_elem.text:
            self._rate = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)').text
        else:
            print(f'Rate not found. Check for errors./n{e.get_attribute("innerHTML")}')
        
        # date
        data_elem = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > span:nth-child(1) > span:nth-child(1)')
        if data_elem.text:
            self._date = data_elem.text.split("-")[0]
        else:
            print(f'Date not found. Check for errors./n{e.get_attribute("innerHTML")}')
        
        # title
        title_elem = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)')
        if title_elem.text:
            self._title = title_elem.text
        else:
            print(f'Title not found. Check for errors./n{e.get_attribute("innerHTML")}')

        # location
        try:
            location = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(2) > span:nth-child(1) > span:nth-child(2) > span:nth-child(1)').text
        except NoSuchElementException:
            location = 'N/A'
        
        if location:
            self._location = location
        else:
            self._location = 'N/A'
        
        # pros
        pr = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > p:nth-child(2) > span:nth-child(1)').text.split()[:40]
        pr = ' '.join(pr)
        self._pros = pr

        # cons
        cn = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > p:nth-child(2) > span:nth-child(1)').text.split()[:40]
        cn = ' '.join(cn)
        self._cons = cn
        
        # recommend
        rec = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1) > svg:nth-child(1)').get_attribute("innerHTML")
        ceo = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(2) > span:nth-child(1) > svg:nth-child(1)').get_attribute("innerHTML")
        bus = e.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > div:nth-child(1) > div:nth-child(3) > span:nth-child(1) > svg:nth-child(1)').get_attribute("innerHTML")
        self._recommend = self.get_vote(rec)
        self._ceo = self.get_vote(ceo)
        self._outlook = self.get_vote(bus)

        # country
        self._country = country

    def __str__(self):
        return f'Review:\nTitle: {self.title}\nLocation: {self.location}\nDate: {self.date}\nRate: {self.rate}\nPros: {self.pros}\nCons: {self.cons}\nRecommend: {self.recommend}\nCEO Approval: {self.ceo}\nBusiness Outlook: {self.outlook}\nCountry: {self.country}\n'
    

    # convert Review instance to dictionary
    def to_dict(self):
        return {
            'Title': self._title,
            'Location': self._location,
            'Date': self._date,
            'Rate': self._rate,
            'Pros': self._pros,
            'Cons': self._cons,
            'Recommend': self._recommend,
            'CEO Approval': self._ceo,
            'Business Outlook': self._outlook,
            'Country': self._country
        }

    def get_vote(self,kw):

        recommend = {
            'M8.835 17.64l-3.959-3.545a1.19 1.19 0 010-1.735 1.326 1.326 0 011.816 0l3.058 2.677 7.558-8.678a1.326 1.326 0 011.816 0 1.19 1.19 0 010 1.736l-8.474 9.546c-.501.479-1.314.479-1.815 0z' : 'approved',
            'M18.299 5.327a1.5 1.5 0 010 2.121l-4.052 4.051 4.052 4.053a1.5 1.5 0 01-2.121 2.121l-4.053-4.052-4.051 4.052a1.5 1.5 0 01-2.122-2.121l4.052-4.053-4.052-4.051a1.5 1.5 0 112.122-2.121l4.05 4.051 4.054-4.051a1.5 1.5 0 012.12 0z' : 'not approved',
            'circle' : 'N/A',
            'rect width="' : 'caution'
            }
        
        for key in recommend:
            if key in kw:
                return recommend[key]
        return 'N/A'


    # getters and setters

    # rate
    @property
    def rate(self):
        return self._rate
    
    @rate.setter
    def rate(self,value):
        self._rate = value

    # date
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self,value):
        self._date = value
    
    # title
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,value):
        self._title = value

    # location
    @property
    def location(self):
        return self._location
    
    @location.setter
    def location(self,value):
        self._location = value

    # pros
    @property
    def pros(self):
        return self._pros
    
    @pros.setter
    def pros(self,value):
        self._pros = value

    # cons
    @property
    def cons(self):
        return self._cons
    
    @cons.setter
    def cons(self,value):
        self._cons = value

    # recommend
    @property
    def recommend(self):
        return self._recommend
    
    @recommend.setter
    def recommend(self,value):
        if isinstance(value,tuple) and len(value) == 3:
            self_recommend = value
        else:
            raise ValueError("Recommend value must be a 3-value tuple")
        
    # ceo approval
    @property
    def ceo(self):
        return self._ceo
    
    @ceo.setter
    def ceo(self,value):
        self._ceo = value

    # business outlook
    @property
    def outlook(self):
        return self._outlook
    
    @outlook.setter
    def outlook(self,value):
        self._outlook(value)
        
    @property
    def country(self):
        return self._country
    
    @country.setter
    def country(self,value):
        self._country = value



class Scraper(Browser):



    def __init__(self,url):

        super().__init__()

        self.url = url
        self.all_reviews = []
        self.country_text = ''
        self.is_skipping = False
        self.last_country = ''
        self.last_page = ''
        self.date_entered = False
        self.start_date = ''
        self.end_date = datetime.now()
        self.stop_flag = True
        self.sure = 'n'
        self.backup_reviews = []
        self.backup_count = 1
        self.review_count = 0
        self.end_review_page_loop = False
        if self.stop_flag:
            print('***Scraper with continuation mode enabled.')
            while('n' in self.sure):
                self.enter_country()
            print(f'Last country stop is {self.last_country}.')
            print(f'Last page stop is {self.last_page}.')

    def enter_country(self):
        self.last_country = input('Enter the country to start scraping: ')
        self.last_page = input('Enter the page to start: ')
        self.sure = input(f'You specified the country: {self.last_country}. Continue? y/n : ')


    def pause(self,min=1):
        time.sleep(min)


    def login(self):
        print("Logging in...")
        self.browser.get("https://www.glassdoor.co.in/index.htm")
        # print(self.browser.page_source)
        self.pause(3)
        #reload if login is slow
        # try:
            # parent = self.browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div/div/div[1]/article/header/nav/div[2]/div/div/div')
            # parent = WebDriverWait(self.browser,20).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div/div/div/div/div[1]/article/header/nav/div[2]/div/div/div')))
            # parent_size = parent.size
            # parent_location = parent.location
            # get all children and display
            # print('***\n'.join([child.tag_name for child in parent.find_elements(By.XPATH,"*")]))
            # from children get the button element
            # button = [child for child in parent.find_elements(By.XPATH,'*') if child.tag_name == 'button'][0]
            # scroll to the button element
            # self.browser.execute_script('arguments[0].scrollIntoView();',button)
            # button = WebDriverWait(self.browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="SiteNav"]/nav/div[2]/div/div/div/button')))
            
            #change the display property to block
            # if button.is_displayed():
            #     print("Button is displayed.")
            # else:
            #     print("Button is not displayed. Modifying property to block")
            #     self.browser.execute_script("arguments[0].style.display = 'block';", button)
                
            # get computed styles
            # css_properties = self.browser.execute_script('var style = window.getComputedStyle(arguments[0]);'
            #                             'var items = {};'
            #                             'for(var i = 0; i < style.length; i++){'
            #                             'var prop = style[i];'
            #                             'items[prop] = style.getPropertyValue(prop);'
            #                             '}'
            #                             'return items;', button)
            
            # print all info
            # print('computedStyle type: {}',type(css_properties))
            # for prop_name,prop_value in css_properties.items():
            #     print(f'{prop_name}:{prop_value}')
            # element_size = button.size
            # element_location = button.location
            # print('Parent size:',parent_size)
            # print('Parent location:',parent_location)
            # print('Element size:',element_size)
            # print('Element location:',element_location)
            
        #     button.click()
        # except NoSuchElementException:
        #     self.browser.refresh()
        #     self.pause()
        #     self.browser.find_element(By.CSS_SELECTOR,'#SiteNav > nav > div.d-none.d-md-block.LockedHomeHeaderStyles__bottomBorder > div > div > div > button').click()
        # except ElementNotInteractableException:
        #     pass

        # self.pause()
        
        
        # user = input("Enter email:")
        self.browser.find_element(By.CSS_SELECTOR,'#inlineUserEmail').send_keys('tamic_888@yahoo.com')
        self.browser.find_element(By.CSS_SELECTOR,'#inlineUserEmail').send_keys(Keys.ENTER)
        self.pause(2)

        # pasw = input("Enter password:")
        self.browser.find_element(By.CSS_SELECTOR,'#inlineUserPassword').send_keys('rgY6n4XKhNUvErt')
        self.browser.find_element(By.CSS_SELECTOR,'#inlineUserPassword').send_keys(Keys.ENTER)
        self.pause(2)
        self.browser.execute_script('window.stop(); ') # stop browser from loading

        # print(f'\nWelcome {user}')
        # prove you're not a bot
        # inp = ''
        # while(inp.lower() != 'done'):
        #     inp = input("Prove you're not a bot if it's asking. Type 'done' when finished: ")


        print(f'Navigating to {self.url}.')
        self.browser.get(self.url)
        self.pause(3)
        

    # export reviews to excel
    def export_reviews_to_excel(self, ls, file_name):
        print('Exporting reviews to an excel file.')
        data = [r.to_dict() for r in ls]
        df = pd.DataFrame(data)
        df.to_excel(file_name, index=False)

    def choose_mode(self):
        inp = input('Continuation mode? y/n: ')
        if 'y' in inp.lower():
            self.stop_flag = True
        elif 'n' in inp.lower():
            self.stop_flag = False
        else:
            self.stop_flag = False

    def run(self):

        self.login()
        # self.sort_by_recent()
        # self.choose_mode()
        self.show_filter()
        self.show_country()
        countries_elem = self.get_countries_elem()
        print(f'There are {len(countries_elem)} locations found.')

        print(', '.join([c.text for c in countries_elem]))
        self.pause(3)

        # loop by country
        for key in range(len(countries_elem)):

            self.country_counter = key

            # check end of date flag is on first before continue
            if self.end_review_page_loop == True:
                print("Stop looping reviews page for this country. End of date reached.")
                self.end_review_page_loop = False # reset end page flag for next country
                continue

            #refresh countries elem if stale
            try:
                print(countries_elem[key].text) # check for stale elem
                country_elem = countries_elem[key]
            except StaleElementReferenceException:
                print(f'Stale country element. Re fetching countries elem..')
                self.show_filter()
                self.show_country()
                try:
                    country_elem = WebDriverWait(self.browser,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div/ul/li')))[key]
                except TimeoutException:
                    country_elem = WebDriverWait(self.browser,2).until(EC.presence_of_all_elements_located((By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[3]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div/ul/li')))[key]
            except TimeoutException:
                print(f'Timed out. Re fetching countries elem..')
                self.browser.refresh()
                self.pause()
                self.show_filter()
                self.show_country()
                country_elem = self.get_countries_elem()[key]


            print(f'Location count: {key}') # show current country count
            
            # reset flag if country elem is found
            if self.last_country.lower() in country_elem.text.lower():
                self.stop_flag = False

            # skip countries if stop flag is True
            if self.stop_flag:
                print('Location not match. Skipping.')
                continue

            # check if location is not a country or empty then skip
            if 'all cities' not in country_elem.text.lower():
                print(f'Country elem text: {country_elem.text} ***')
                print('Not a country. Skipping..')
                continue
            else:
                self.country_text = country_elem.text.lower().replace('- all cities','').strip().title() #get country_text
                print(f'\nCountry select: {self.country_text} ***') 
                self.browser.execute_script('arguments[0].scrollIntoView();',country_elem) # scroll into country_elem
                self.country_select(country_elem,key)
                self.pause(10)
                
            # enter date range
            if self.date_entered == False: # ask user input if date is datetime object and length of all_reviews is greater than 0
                self.date_entered = True
                start_date = input('Enter start date (dd mm yyyy): ')
                end_date = input('Enter end date (dd mm yyyy): ')
                if start_date:
                    self.start_date = datetime.strptime(start_date, '%d %m %Y')
                else:
                    self.start_date = datetime.strptime('01 01 1900', '%m %d %Y')
                if end_date:
                    self.end_date = datetime.strptime(end_date, '%d %m %Y')
                else:
                    self.end_date = datetime.now()

            # convert end_date to datetime obj
            if not isinstance(self.end_date,datetime):
                print('Resetting end date?')
                self.end_date = datetime.now() # reset start_date immediately
                self.pause()

            # check last review page - continue last page from interruption - check if review last_page is specified and start scraping there
            if self.last_page == '':
                review_page_num = 1
                
            else:
                
                review_page_num = float(self.last_page) # convert page num to float
                print(f'Begin scraping in page {review_page_num}.')

                url_start_page = self.browser.current_url.replace('.htm',f'_IP{self.last_page}.htm') # get url ready
                print(f'{url_start_page}')
                self.browser.get(url_start_page)
                self.pause(10)

                # reset review page flag
                self.last_page = ''


            print(f'Page number - {review_page_num}')



            # check if reviews are available. skip if 0
            if self.get_total_reviews() > 0:
                # get reviews
                self.get_page_reviews()

                # loop review pages
                review_page_lang = review_page_num # assign last page flag - set review_page_num to current language pages
                while(self.next_page()):
                    print(f'Page number - {review_page_lang}')
                    if self.end_review_page_loop == True:
                        print('Stopping as the start date is reached.')
                        break
                    self.get_page_reviews()
                    review_page_lang += 1
                review_page_lang = review_page_num

                # loop languages
                while(self.select_next_language()):
                    print('Switching to next language')
                    
                    # check if reviews for this language are available
                    if self.get_total_reviews() > 0:
                        # get reviews
                        self.get_page_reviews()

                        # loop review page
                        while(self.next_page()):
                            print(f'Page number - {review_page_lang}')
                            if self.end_review_page_loop == True:
                                print('Stopping as the start date is reached.')
                                break
                            self.get_page_reviews()
                            review_page_lang += 1
                    else:
                        print('No reviews for this language.')
                        continue
            else:
                print('No reviews for this country. Skipping.')
                continue

            self.clear_country()

        self.export_reviews_to_excel(self.all_reviews,'glassdoor_reviews.xlsx')
        print('Data saved and done.')


    def select_next_language(self):
    # Selects the next language in a dropdown menu.

    # Returns:
    #     str: The text of the selected language.

    #     None: If the language cannot be selected.
        self.show_filter()
        self.show_language()
        try:
            # Find the language dropdown element
            try:
                self.browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul')
                language_dropdown = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul')
            except NoSuchElementException:
                language_dropdown = self.browser.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/main/div[1]/div[3]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/ul')

            # Find the currently selected language element
            current_language = language_dropdown.find_element(By.CSS_SELECTOR, '.checked')

            # Find the next language element by navigating the DOM
            next_language = current_language.find_element(By.XPATH, 'following-sibling::li')

            # Click the next language element
            next_language.click()

            # Pause briefly to allow the page to update
            self.pause(3)

            # Return the text of the selected language
            return True

        except (NoSuchElementException, ElementNotInteractableException):
            # The language dropdown or next language element could not be found, return None
            return False


    def sort_by_oldest(self):
        print('Sort by oldest')
        url = self.browser.current_url.replace('ascending=false','ascending=true')
        self.browser.get(url)
        self.pause(5)

    def sort_by_recent(self):
        print('Sort by most recent')
        try:
            self.browser.find_element(By.CSS_SELECTOR,'div.ml-sm > div:nth-child(2)').click() # expand dropdown
        except NoSuchElementException:
            self.browser.refresh()
            self.pause(5)
            self.browser.find_element(By.CSS_SELECTOR,'div.ml-sm > div:nth-child(2)').click() # expand dropdown
        self.pause(2)
        self.browser.find_element(By.CSS_SELECTOR,'#option_DATE > span:nth-child(2)').click() # select sort by recent
        # self.browser.find_element(By.CSS_SELECTOR,'#option_DATE').send_keys(Keys.ENTER) # select sort by recent
        self.pause(10)

    def country_select(self,obj,key):
        print('Selecting country...')
        # print(f'drodown innerhtml:{obj.get_attribute("innerHTML")}')
        print(f'Country to compare: {self.country_text}')
        print(f'Country elem text: {obj.text}')
        if self.country_text.lower() in obj.text.lower():
            print('Country match. Selecting..')
            try:
                self.browser.execute_script('arguments[0].scrollIntoView();',obj)
                obj.click() # select
            except StaleElementReferenceException:
                print('Stale country elem upon clicking.')
                self.show_filter()
                self.show_country()
                obj.click()
            except ElementClickInterceptedException:
                print('Country elem not clickable.')
                self.browser.refresh()
                self.pause(3)
                self.show_filter()
                self.show_country()
                self.get_countries_elem()[key].click()
            except:
                self.show_filter()
                self.show_country()
                print('Inputting country text directly.')
                self.browser.find_element(By.CSS_SELECTOR,'.typeToFilterInput > div:nth-child(1) > input:nth-child(1)').send_keys(self.country_text)
                self.browser.find_element(By.CSS_SELECTOR,'.typeToFilterInput > div:nth-child(1) > input:nth-child(1)').send_keys(Keys.ENTER)

        else:
            print('No match getting countries with keyword param')
            raise ValueError('No matching "all cities" in countries_elem. Check css selectors for countries elem.')
            # self.get_countries_elem(self.country_text)[0].click() # select (with keyword)
        self.pause()

    def get_countries_elem(self,kw=''):  # with kw, this will return narrowed down result with keyword as filter        
        
        # get all countries
        # countries_elem = self.browser.find_elements(By.CSS_SELECTOR,'.dropdownExpanded > div:nth-child(1) > ul > li')
        countries_elem = WebDriverWait(self.browser,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'.dropdownExpanded > div:nth-child(1) > ul > li')))

        # check if all cities is present
        all_cities_elem = [c for c in countries_elem if 'all cities' in c.text.lower()]
        if not all_cities_elem:
            raise ValueError('Could not find all cities kw on elems. Check filter and dropdown toggled.')

        # filter countries based on keyword
        if kw:
            countries_elem = [c for c in countries_elem if kw.lower() in c.text.lower()]
        
        # print(', '.join([c.text for c in countries_elem]))
        return countries_elem

    def next_page(self):
        current = self.current_page()
        print(f'Current page: {current}')
        total_page = self.get_total_reviews()
        print(f'total page: {total_page}')
        # self.pause(3)

        # check if pagination exists
        try:
            btn = WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.nextButton')))
            self.browser.execute_script('arguments[0].scrollIntoView();', btn)
        except TimeoutException:
            # self.browser.refresh()
            # self.pause()
            # btn = WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.nextButton')))
            # self.browser.execute_script('arguments[0].scrollIntoView();', btn)
            return False
        except NoSuchElementException:
            return False
        
        if current != total_page: # logic to go click next page or not
            print(f'Last page not reached yet. Attempt click..')
            try:
                self.browser.execute_script('arguments[0].scrollIntoView();',self.browser.find_element(By.CSS_SELECTOR,'.nextButton'))
                
                # hide sticky nav (intercepts the pagination button)
                stikynav = self.browser.find_element(By.CSS_SELECTOR,'#StickyNavWrapper')
                # navparent= stikynav.find_element(By.XPATH,'..')
                self.browser.execute_script('arguments[0].style.visibility = "hidden";',stikynav)
                # self.pause(5)

                WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.nextButton'))).click()
            except ElementClickInterceptedException:
                print(f'Next button unclickable. Attempting to navigate next page by url manipulation.')
                if current > 10:
                    url = self.browser.current_url.replace(f'_IP{current}.htm',f'_IP{int(current)+1}.htm')
                else:
                    url = self.browser.current_url.replace(f'.htm',f'_IP{int(current)+1}.htm')
                print(url)
                self.browser.get(url)
                self.pause(5)

            self.pause(10)
            print(f'Current page: {current}')
            print(f'Total page: {total_page}')
            return True
        else:
            print('Pagination exhausted.')
            return False

    def get_pagination_footer(self):
        try:
            footer = WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.paginationFooter'))).text
            return footer
        except (NoSuchElementException, TimeoutException):
            while True: # infinite loop (exercise caution)
                try:
                    self.browser.refresh()
                    self.pause()
                    footer = WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#ReviewsRef + div'))).text
                    return footer
                except:
                    print("Timed out getting footer. Re looping until successful.")
                    continue

    def get_total_reviews(self):
        footer = self.get_pagination_footer()
        print(f'{footer}')
        if len(footer.lower().split()) == 8:
            return float(footer.split()[-3])
        else:
            return float(footer.replace(',','').split()[-2])
    
    def current_page(self):
        footer = self.get_pagination_footer().strip()
        print(footer.split())
        # if 'english' in footer.lower():
        if len(footer.lower().split()) == 8:
            return float(footer.split()[-5])
        else:
            return float(footer.split()[-4])

    def clear_country(self):
        print("Resetting country.")
        self.browser.get(self.url)
        self.pause(2)

    def is_filter_expanded(self):
        try:
            # WebDriverWait(self.browser,3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Container"]/div[1]/div[2]/main/div[1]/div[3]/div/div[1]/div[3]')))
            WebDriverWait(self.browser,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#Container > div.container-max-width.mx-auto.px-0.px-lg-lg.py-lg-xxl > div:nth-child(2) > main > div.eiReviews__EIReviewsPageStyles__EIReviewsPage.pt-0.pr-std.pb-std.pl-std.p-md-std.css-d4t0ju.els8ktd0.gd-ui-module.css-rntt2a.ec4dwm00 > div.eiReviews__EIReviewsPageStyles__filterDropdown > div > div.search > div.dropdownsContainer.lib__EIFilterModuleStyles__desktopDropdowns.d-none.pt-sm.pr-xl.pb-std.pl-md')))
            # WebDriverWait(self.browser,3).until(EC.presence_of_element_located((By.CSS_SELECTOR,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[@class="d-none"]')))
            return False
        except:
            return True

    # expands filter and show all sort of filter options
    def show_filter(self):
        while True: #infinite loop (exercise caution)
            try:
                if self.is_filter_expanded():
                    print('Filter shown.')
                else:
                    print("Expanding filter.")
                    try:
                        self.browser.find_element(By.CSS_SELECTOR,'button.d-none > span:nth-child(1) > div:nth-child(1)').click()
                        # self.browser.find_element(By.CSS_SELECTOR,'button[data-text="ContentFiltersFilterToggleBtn"]').click()
                        # WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button[data-text="ContentFiltersFilterToggleBtn"]'))).click()
                        print("Filter expanded.")
                    except NoSuchElementException as e:
                        print("No such element exception raised for clicking filter.")
                        # WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[2]/div[2]/button'))).click()
                        WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Container"]/div[1]/div[2]/main/div[1]/div[3]/div/div[1]/div[2]/div[2]/button'))).click()
                    except ElementClickInterceptedException as e:
                        print(f'Click intercepted exception raised for clicking filter. Refreshing...')
                        self.browser.refresh()
                        self.pause(5)
                        WebDriverWait(self.browser,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,'button.d-none > span:nth-child(1) > div:nth-child(1)'))).click()
                break
            except:
                print("Re looping show_filter function.")
                continue
                
            # except TimeoutException as e:
            #     print('Timed out exception raised for clicking filter.')
                #code here

        # self.pause()
    
    def show_language(self):
        while True: # infinite loop (exercise caution)
            try:
                print('Showing languages.')
                try:
                    WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[2]'))).click()
                except TimeoutException:
                    print('Timeout exception occurred after attempt to toggle language dropdown.')
                    print('Filter collapsed? Showing filter...')
                    # self.browser.refresh()
                    # self.pause()
                    self.show_filter()
                    WebDriverWait(self.browser,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div/div/div[1]/div[3]/div[2]/div[2]'))).click()
                # print("Displaying languages.")
                #     WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div select[aria-label=language] + div'))).click()
                # except:
                #     WebDriverWait(self.browser,5).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[2]'))).click()
                break
            except:
                print('Re looping show_language')
                continue

    # show all countries by clicking the country filter and a dropdown of countries will expand
    def show_country(self):
        print("Showing countries.")
        # check if countries already shown
        # try:
        #     self.browser.find_element(By.CSS_SELECTOR,'div.pl-md-xsm:nth-child(2) > div:nth-child(1)').click() # interact the div to activate the select dropdown
        # except NoSuchElementException:
            # self.browser.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[1]').click()
        # except ElementNotInteractableException:
        #     self.show_filter()
        #     self.browser.find_element(By.CSS_SELECTOR,'div.pl-md-xsm:nth-child(2) > div:nth-child(1)').click()
        try:
            self.browser.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[1]').click()
        except NoSuchElementException:
            self.show_filter()
            try:
                self.browser.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[1]/div/div[1]/div[3]/div[2]/div[1]').click()
            except NoSuchElementException:
                self.browser.find_element(By.XPATH,'/html/body/div[2]/div[1]/div[2]/main/div[1]/div[3]/div/div[1]/div[3]/div[2]/div[1]').click()

        # self.browser.find_element(By.CSS_SELECTOR,'.typeToFilterInput > div:nth-child(1) > input:nth-child(1)').click() # click the activated div > input
        # self.pause()
        
        self.pause()
    
    def add_backup_reviews(self,r):
        self.backup_reviews.append(r)

    # checks date in a list of review elements (by end date)
    def is_date_found(self,r):
        d = r.date.split()
        r_date = ' '.join([d[0],d[1][:3],d[2]])
        print(f'Checking date: {r.date}')
        r_date = datetime.strptime(r_date,'%d %b %Y')
        if r_date <= self.end_date:
            return True
        return False

    def skip_to_reviews_by_date(self):
        reviews_elem = self.get_reviews_elem()
        if self.is_date_found(reviews_elem):
            print('End date starts here.')
            return
        
        while(self.next_page()):
            reviews_elem = self.get_reviews_elem()
            if self.is_date_found(reviews_elem):
                print('End date starts here.')
                return

        
    # returns review elements in a page
    def get_reviews_elem(self):
        # return self.browser.find_elements(By.CSS_SELECTOR,'li.noBorder')
        try:
            return WebDriverWait(self.browser,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'li.noBorder')))
        except TimeoutException:
            print(f'No reviews available for {self.country_text}')
            return []


    def is_start_date_found(self,r):
        # check start date and stop fetching reviews
        if isinstance(self.start_date,datetime):
                print(r.date)
                # prepare convert date to datetime obj
                date = r.date.split()
                month = date[1] if len(date[1]) < 4 else date[1][:3]
                date_str = ' '.join([date[0],month,date[2]])
                # check start date logic
                try:
                    if datetime.strptime(date_str,'%d %b %Y') <= self.start_date:
                        print('Start date reached.')
                        self.end_review_page_loop = True
                        return True# stop getting reviews past start date
                except ValueError:
                    if datetime.strptime(date_str,'%d %B %Y') <= self.start_date:
                        print('Start date reached.')
                        self.end_review_page_loop = True
                        return True# stop getting reviews past start date

    def get_page_reviews(self):
        print("Getting reviews for this page.")

        reviews_elem = self.get_reviews_elem()
        
        # check if reviews are available
        if len(reviews_elem) == 0:
            print('No reviews for this page')
            return
        
        print(f'There are {len(reviews_elem)} review(s) found in this page.')


        # loop reviews
        for count,elem in enumerate(reviews_elem):
            print(f'Review number {count+1}')

            # Review class instance
            try:
                elem.find_element(By.CSS_SELECTOR,'li.noBorder > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)')
                r = Review(elem,self.country_text)
            except TimeoutException: # refresh browser and re fetch reviews elem
                self.browser.refresh()
                self.pause(3)
                elem = WebDriverWait(self.browser,5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'li.noBorder')))[count]
                r = Review(elem,self.country_text)

            # check end_date and start there
            if not self.is_date_found(r):
                print(r.date)
                continue
            # else:
            # print('End date found. Start getting reviews.')
            #     self.pause()

            # start gathering reviews for backing up
            self.add_backup_reviews(r)
            self.review_count += 1

            # start actual backup if it reached 300
            if self.review_count == 300:
                print(f'Backing up reviews.')
                self.export_reviews_to_excel(self.backup_reviews,f'glassdoor_reviews_backup_{self.backup_count}.xlsx')
                self.review_count = 0 #reset counter
                self.backup_count += 1
                self.backup_reviews = []
                print(f'backup_count: {self.backup_count}')
                self.pause()

            # check start date and stop fetching reviews
            if self.is_start_date_found(r):
                return
            
            print(r)

            self.all_reviews.append(r)
        


if __name__ == '__main__':

    url = 'https://www.glassdoor.co.in/Reviews/Publicis-Sapient-Reviews-E1646026.htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng&filter.employmentStatus=REGULAR&filter.employmentStatus=PART_TIME'
    scraper = Scraper(url)
    # try:
    scraper.run()
    # except Exception as e:
    #     logging.error('Error: %s',str(e))
    #     print(f'Scraper interrupted: {e}')
    #     scraper.export_reviews_to_excel(scraper.all_reviews,'glassdoor_reviews.xlsx')
    # finally:
    #     pass