
import os, sys, shutil, xlrd, time, csv, xlwt
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import webdriver_config as driver

vendor = sys.argv[1]
v_code = sys.argv[2]


br = driver.init_driver()

def vendor_file(v):
    with open("C:\Users\Berries\Code\csv\outfile\\vendor_ids.csv","r") as infile:
        reader = csv.reader(infile)
        for line in reader:
            if v in line[0]:
                print line[7]
                return line[7]


def go_to_home():
    os.chdir("C:\Users\Berries\Code\csv\outfile")

def go_to_shst():

	dir = os.getcwd()
	
	if dir == "C:\\Users\\Berries\\Code":
		dest = "C:\Dropbox\SHST Files\BRANDS Updated Sheet 2019\\"
	else:
		dest = "F:/Dropbox/SHST Files/SHST Updated Sheet/"
	os.chdir(dest)
    
	print os.getcwd()
	return dest
	
	# return dest+latest
	
def get_uploaded_images():
    
    try:
        WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div.menu > ul > li.dropdownList.hidden-xs.menu-dropdown-icon > ul > div > li:nth-child(1) > ul > li:nth-child(3) > a"))).click()
    except:
        time.sleep(1)
        pass
    
    time.sleep(30)
    
    print "Scanning all images..."
    uploaded_images = [img.text for img in br.find_elements_by_css_selector("#basic_html > div > div > div > div > div.Product_content.text-center > label")]
    print "Total number of uploaded images:"
    print len(uploaded_images)
    print  uploaded_images
    return uploaded_images

	# br.execute_script("window.stop();")
	# btn.send_keys(dir+vendor_file(vendor.split()[0].lower()))
	# btn.submit()
	
	
def con():
    rbook = xlrd.open_workbook("./csv/outfile/Brands SHST Master sheet.xls")
    rsheet = rbook.sheet_by_index(0)
    for x in range(rsheet.nrows):
        row = rsheet.row(x)
        if row[0].value == vendor:
            print row[0].value
            return [row[1].value,row[2].value]
	

def output_missing(ls):
    go_to_home()
    with open("shst_missing_images.csv","w") as outfile:
        print os.getcwd()
        writer = csv.writer(outfile)
        for line in ls:
            # print line
            writer.writerow([line])

        outfile.close()

def get_vendor_images(my_dir):

    # print my_dir+vendor_file(vendor.split()[0].lower())

    rbook = xlrd.open_workbook(my_dir+vendor_file(v_code))
    rsheet = rbook.sheet_by_index(0)
    return [rsheet.row(x)[13].value for x in range(rsheet.nrows)]

def login(un,pw):
	print "Logging in"
	# WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div > ul > li.dropdownList.menu-dropdown-icon > a"))).click()
	# WebDriverWait(br,5).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div > section.header_section > div > div > div.col-lg-9.col-sm-12.col-md-9 > div.menu > ul > li.dropdownList.hidden-xs"))).click()
	time.sleep(1)
	br.find_element_by_name("email").send_keys(un)
	br.find_element_by_name("password").send_keys(pw)
	br.find_element_by_name("password").send_keys(Keys.ENTER)
	time.sleep(1)
	print "Accessed."

def main():
    
    url = "https://www.shophereshopthere.com/"
    
    uname = ""
    passw = ""
    missing = []
    
    br.get(url)
    time.sleep(1)

    uname,passw = con()
    # book = xlrd.open_workbook("./csv/outfile/Brands SHST Master sheet.xls")
    # rsheet = book.sheet_by_index(0)
    # for x in range(rsheet.nrows):
    #     print rsheet.row(x)


    login(uname,passw)
    
    current_dir = go_to_shst()

    vendor_images = get_vendor_images(current_dir)
    print vendor_images
    print "...Vendor images"
    time.sleep(5)
    uploaded = get_uploaded_images()
    
    print "Action: Check for missing images."
    for img in vendor_images:
        if img not in uploaded:
            # print img
            missing.append(img)
            
    output_missing(missing)
	
if __name__ == "__main__":
	main()