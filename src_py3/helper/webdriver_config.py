import os
import time
import random

#chrome driver loader
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
# from selenium_stealth import stealth

import undetected_chromedriver as uc

# capa = DesiredCapabilities.CHROME

# capa = DesiredCapabilities().FIREFOX
# capa['marionette'] = False

# capa["pageLoadStrategy"] = 'none'

def init_driver():
    # path = os.path.dirname(__file__)+'/chrome_driver/chromedriver'
    # browser = webdriver.Chrome(executable_path = path,desired_capabilities = capa)
    chrome_options = uc.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_experimental_option('excludeSwitches',["enable-automation"])
    # Instead of excludeSwitches, you might want to add these arguments directly
    # chrome_options.add_argument("--profile-directory=Default")
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    # chrome_options.add_argument(f'--user-agent={user_agent}')
    headless = input("Do you like to run in --headless mode? [y/n]")
    if('y' in headless.lower()):
        chrome_options.add_argument('--headless')
        print("confirmed --headless mode")
        chrome_options.add_argument('--window-size=1920,924') # set viewport size
        # chrome_options.add_argument('--user-data-dir=file:///C:/Users/USER/AppData/Local/Google/Chrome/User%20Data/Default/') 
    
    # browser = webdriver.Chrome(options=chrome_options)#executable_path = path)#, options=chrome_options)
    browser = uc.Chrome(options=chrome_options,use_subprocess=True)#executable_path = path)#, options=chrome_options)
    
    # Apply selenium-stealth to the driver
    # stealth(browser,
    #         languages=["en-US", "en"],
    #         vendor="Google Inc.",
    #         platform="Win32",
    #         webgl_vendor="Intel Inc.",
    #         renderer="Intel Iris OpenGL Engine",
    #         fix_hairline=True,
    #         run_on_insecure_origins=False
    # )
	
    # path = './firefox_driver/geckodriver'
    # browser = webdriver.Firefox(executable_path = path,desired_capabilities = capa)
	
    browser.wait = WebDriverWait(browser,5)
    browser.delete_all_cookies()
    # browser.execute_script("window.resizeTo(screen.width,screen.height)")
    #maximize window
    browser.maximize_window()
    time.sleep(random.uniform(1,3))
    return browser