import sys,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException

class Browser:
    
    def __init__(self,url):
        self.delay = 5
        path = './firefox_driver/geckodriver'
        self.browser = webdriver.Firefox(executable_path=path)
        self.browser.maximize_window()
        self.browser.get(url)

class Scraper(Browser):

    def __init__(self,url):
        Browser.__init__(self,url)
        self.results = []
        self.counter = 0
        self.final = []
        time.sleep(2)

    def get_all_designers_by_zip(self,zip):
        page_results = self.search_zip(zip)
        print(page_results)
        self.results.extend(page_results)
        while(self.is_next_page_available()): #starts pagination
            try:
                page_results = self.grab_page_designers()
                print(page_results)
                self.results.extend(page_results)
            except:
                print("End of pages reached.")
                break

        return self.results

        
    # utilize search feature to seek designers by zip code - return a list of a tags
    def search_zip(self,zip):
        try:
            selector = ".pro-location-autosuggest__input" #selector choice for search feature
            self.browser.find_element_by_css_selector(selector)
        except NoSuchElementException:
            selector = "#hui-text-input-1"

        try:
            self.browser.find_element_by_css_selector("#hz-page-content-wrapper > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > span:nth-child(1) > a:nth-child(1)").click() # select new york - go to default search page choice
            time.sleep(self.delay) # delay 1 sec to load page
        except NoSuchElementException:
            print("")

        try:
            self.browser.find_element_by_css_selector(selector).clear()
        except NoSuchElementException:
            selector = ".pro-location-autosuggest__input" #selector choice for search feature
        self.browser.find_element_by_css_selector(selector).clear()
        self.browser.find_element_by_css_selector(selector).send_keys(zip)
        self.browser.find_element_by_css_selector(selector).send_keys(Keys.ENTER)
        time.sleep(self.delay) # delay 1 sec to load page

        
        return self.grab_page_designers()
    
    def grab_page_designers(self):
        try:
            return [a.get_attribute("href") for a in self.browser.find_elements_by_css_selector("li.hz-pro-search-results__item > div:nth-child(1) > a:nth-child(1)")]
        except StaleElementReferenceException: # reload in case of stale element
            self.browser.refresh()
            time.sleep(self.delay)
            return [a.get_attribute("href") for a in self.browser.find_elements_by_css_selector("li.hz-pro-search-results__item > div:nth-child(1) > a:nth-child(1)")]
    
    def is_next_page_available(self):
        try:
            if self.counter > 2:#stop after x pages for testing purposes
                return False
            try:
                self.browser.find_element_by_css_selector("div.directory-results-pagination:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(10) > span:nth-child(1) > span:nth-child(1)").click()
            except NoSuchElementException:
                self.browser.find_element_by_css_selector("a.hz-pagination-link:nth-child(11)").click()
            print("Navigating page..")
            time.sleep(self.delay)
            self.counter+=1
            return True
        except NoSuchElementException:
            print("End of pagination reached.")
            return False
        
    def scrape_sites_built_by_houzz(self,results,keyword):
        for res in results: #loop each link and find the keyword
            self.browser.get(res)
            time.sleep(self.delay)

            try:
                link = self.browser.find_element_by_css_selector("#business > div:nth-child(2) > div:nth-child(3) > p:nth-child(2) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1)").text #grab the designer's url
            except NoSuchElementException:
                print "This designer has no link available."
                continue
            try:
                self.browser.get("https://"+link)
            except WebDriverException: #handle errors for loading pages
                print("Error loading page.")
                continue
            time.sleep(self.delay)
            
            #search for specific keywords
            html = self.browser.execute_script("return document.body.innerHTML") 
            if keyword in html:
                self.final.append(res)
                print("%s added to the list. This website is built on houzz.\n" %res)
            else:
                print("Keyword not detected in %s. This website is not built by houzz.\m" %res)
            






if __name__ == '__main__':
    url = "https://www.houzz.com/professionals/interior-designer/"
    scraper = Scraper(url)

    # zip = [6307, 10001, 10002]
    # https://www.houzz.com/for-pros/software-interior-designer-custom-website
    z = raw_input("Enter zip:")
    results = scraper.get_all_designers_by_zip(z)
    kw = raw_input("Enter the url to search:")
    scraper.scrape_sites_built_by_houzz(results,kw)
    print("Here are the results in text:")
    for url in scraper.final:
        print("%s" %url)