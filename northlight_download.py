
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

class domain:
	
	url = "https://northlightseasonal.com/"
	uname = "rick@waresitat.com"
	passw = "wolfville"
	browser = None
	
	def __init__(self):
		path = "./chrome_driver/chromedriver"
		self.browser = webdriver.Chrome(executable_path = path)
		self.browser.wait = WebDriverWait(self.browser, 5)
		self.browser.maximize_window()
		
		# self.login(browser,self.uname,self.passw)

		# return browser



	def login(self,un,pw):
		print "Logging in."
		self.browser.get(self.url)
		time.sleep(3)
		
		self.browser.find_element_by_css_selector("#privy-inner-container > div:nth-child(1) > div > div.privy-popup-inner-content-wrap > div.privy-dismiss-content > div").click()
		time.sleep(1)
		
		self.browser.find_element_by_css_selector("#shoplogo span.custlogin a").click()
		time.sleep(1)
		
		self.browser.find_element_by_css_selector("#customer_email").send_keys(un)
		self.browser.find_element_by_css_selector("#customer_password").send_keys(pw)
		self.browser.find_element_by_css_selector("#customer_password").send_keys(Keys.ENTER)
		print "Success."
	
	
	
	
	
def main():
	br = domain()
	br.login(br.uname,br.passw)
	
	
	
if __name__ == "__main__":
	main()
	