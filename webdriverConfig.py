##chrome driver loader
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import webdriver_config
from selenium.webdriver.support.ui import WebDriverWait

capa = DesiredCapabilities.CHROME

# capa = DesiredCapabilities().FIREFOX
# capa['marionette'] = False

# capa["pageLoadStrategy"] = 'none'

def initDriver():
    path = './chrome_driver/chromedriver'
    # browser = webdriver.Chrome(executable_path = path,desired_capabilities = capa)
    browser = webdriver.Chrome(executable_path = path)
	
    # path = './firefox_driver/geckodriver'
    # browser = webdriver.Firefox(executable_path = path,desired_capabilities = capa)
	
    browser.wait = WebDriverWait(browser,5)
    # browser.execute_script("window.resizeTo(screen.width,screen.height)")
    #maximize window
    browser.maximize_window()
    return browser