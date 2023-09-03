import sqlite3,os,sys,shutil,csv,time
import webdriver_config
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def login(br,uname,passw):
	br.find_element_by_id("sign-up-in").click()
	time.sleep(5)
	br.find_element_by_css_selector("input[name=login_email]").send_keys(uname)
	br.find_element_by_css_selector("input[name=login_password]").send_keys(passw)
	br.find_element_by_css_selector("input[name=login_password]").send_keys(Keys.ENTER)
	time.sleep(5)
	# WebDriverWait(br, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "login_email"))).send_keys(uname)
	time.sleep(3)
	
def isDownloaded(img):
	files = os.listdir("C:\Users\Berries\Documents\Downloads")
	print files
	for file in files:
		if img in file:
			print img+" EQUAL to "+file
			print img+" detected on the list! Proceeding..."
			return True
		else:
			print img+" not equal to "+ file
			print img+" NOT detected on the list."
			# time.sleep(.5)
	return False

def search(key):
	print key
	br.find_element_by_css_selector("input[placeholder=Search]").clear()
	br.find_element_by_css_selector("input[placeholder=Search]").send_keys(key)
	br.find_element_by_css_selector("input[placeholder=Search]").send_keys(" ")
	time.sleep(3)
	try:
		link = WebDriverWait(br, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#embedded-app > div > div.maestro-chrome.maestro-chrome--search.maestro-chrome--search-active > div.maestro-app > div.maestro-app-content > div.search__view.maestro-content-scroll > div > div.search-results > div > div:nth-child(1) > div > table > tbody > tr")))
		return link
	except:
		print "Item not found."
		return None


def create_table():
	try:
		con = sqlite3.connect('waresitat.db')
		cur = con.cursor()
		cur.execute("create table if not exists dropbox_out('sku text not null','link text not null');")
		con.commit()
		
	except sqlite3.Error,e:
		print "Error %s" % e.args[0]
		
	finally:

		if con:
			con.close()

def expand_sidebar():
	print "Expanding sidebar."
	br.find_element_by_css_selector("#browse-react-file-viewer-container > div > div > div > div > div.react-file-viewer__main > div.react-file-viewer__sidebar.react-file-viewer__sidebar--closed > aside > div > div.mc-positioned-portal-wrapper > button").click()
	time.sleep(1)

def expand_download():
	print "Getting ready for download."
	br.find_element_by_css_selector("#embedded-app > div > div.maestro-chrome.maestro-chrome--search.maestro-chrome--search-active > div.maestro-app > div.maestro-app-content > div.search__view.maestro-content-scroll > div > div.search-results > div > div:nth-child(1) > div > table > tbody > tr > td.mc-table-cell.mc-media-cell.mc-media-cell-double-line.brws-file-modified-at-cell > div.mc-media-actions > div.browse-overflow-menu > div > div").click()
	time.sleep(1)

def click_download():
	print "Downloading.."
	br.find_element_by_css_selector("body > div.mc-positioned-portal-content > div > div > div > div > div > span.action-download.mc-popover-content-item").click()
	time.sleep(1)


def get_image(link,row):
	
	# link.click()
	time.sleep(1)
		
	# expand_sidebar()
	expand_download()
	
	click_download()
	
	time.sleep(3)
	
	while not isDownloaded(row):
		time.sleep(1)
		continue
		
	
def perform_insert(arr):
	table.append(arr)


def gotoFolder():
	br.get(url)
	time.sleep(1)
	br.find_element_by_css_selector("#files").click()
	time.sleep(1)
	br.find_element_by_link_text("A Cheerful Giver Web Images (1)").click() # folder to search
	time.sleep(1)



br = webdriver_config.init_driver() # initialize webdriver
	
def main():	

	user,pasw,vendor = sys.argv[1],sys.argv[2],sys.argv[3] # get username and pass and vendor
	url = "https://www.dropbox.com/"
		
	file = open("./csv/outfile/noimg/"+vendor+".csv",'rb') # open csv file of vendor missing images
	fread = csv.reader(file)

	table = []
	print user,pasw

	br.get(url)
	time.sleep(1)

	login(br,user,pasw) # login
	time.sleep(5)

	inp = raw_input("Please verify. Answer when done: ") # Checking youre robot.
	if inp.lower() in "y":
		pass
	else:
		raise

	br.find_element_by_css_selector("#files").click() # Navigate dropbox folder
	time.sleep(1)

	# for handle in br.window_handles:
	# 	br.switch_to_window(handle)

	# create_table()

	for row in fread:
		print "Getting item."
		# gotoFolder()
		br.get("https://www.dropbox.com/home/A%20Cheerful%20Giver%20Web%20Images%20(1)")
		time.sleep(2)
		item = search(row[0])

		if item!= None:
			get_image(item,row[0]) # download image

			time.sleep(1)
			
	outfile = open("./csv/outfile/dropbox_output.csv","wb")
	writer = csv.writer(outfile)
	writer.writerows(table)
	outfile.close()

	print "Job Done."
	sys.exit()	
	br.close()

if __name__ == "__main__":
	main()