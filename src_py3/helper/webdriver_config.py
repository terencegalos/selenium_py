import os

#chrome driver loader
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

capa = DesiredCapabilities.CHROME

# capa = DesiredCapabilities().FIREFOX
# capa['marionette'] = False

# capa["pageLoadStrategy"] = 'none'

def init_driver():
    path = os.path.dirname(__file__)+'/chrome_driver/chromedriver'
    # browser = webdriver.Chrome(executable_path = path,desired_capabilities = capa)
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    chrome_options.add_argument('--user-agent={user_agent}')
    chrome_options.add_argument('--window-size=1920,924') # set viewport size
    
    browser = webdriver.Chrome()#executable_path = path)#, options=chrome_options)
	
    # path = './firefox_driver/geckodriver'
    # browser = webdriver.Firefox(executable_path = path,desired_capabilities = capa)
	
    browser.wait = WebDriverWait(browser,5)
    # browser.execute_script("window.resizeTo(screen.width,screen.height)")
    #maximize window
    browser.maximize_window()
    return browser