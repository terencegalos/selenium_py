from helper.table_gateway import gateway
from helper.domainobject import domainobject
import datetime,csv,os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException as StateElementReferenceException

class ragon(domainobject):
    
    def __init__(self,driver,scraper_mode):
        super().__init__(driver)
        self.mode = scraper_mode
        self.resume_file = os.path.join(os.path.dirname(__file__), "..", "resume", f"{self.vendor.replace('/', '_')}_resume.txt")
        self.last_processed_url = None
        self._ensure_resume_directory()
        self.mode = scraper_mode
        self.resume_file = os.path.join(os.path.dirname(__file__), "..", "resume", f"{self.vendor.replace('/', '_')}_resume.txt")
        self.last_processed_url = None
        self._ensure_resume_directory()
        self.load_resume_point()  # Load resume point for all modes

    def _ensure_resume_directory(self):
        """Ensure the resume directory exists"""
        resume_dir = os.path.dirname(self.resume_file)
        if not os.path.exists(resume_dir):
            os.makedirs(resume_dir)

    def save_resume_point(self, url):
        """Save the last processed URL for resume functionality"""
        try:
            with open(self.resume_file, 'w', encoding='utf-8') as f:
                f.write(url)
            self.last_processed_url = url
            print(f"💾 Resume point saved: {url}")
        except Exception as e:
            print(f"Warning: Could not save resume point: {e}")

    def load_resume_point(self):
        """Load the last processed URL from resume file"""
        try:
            if os.path.exists(self.resume_file):
                with open(self.resume_file, 'r', encoding='utf-8') as f:
                    url = f.read().strip()
                    if url:
                        self.last_processed_url = url
                        print(f"📖 Resume point loaded: {url}")
                        return url
        except Exception as e:
            print(f"Warning: Could not load resume point: {e}")
        return None

    def clear_resume_point(self):
        """Clear the resume file when scraping is complete"""
        try:
            if os.path.exists(self.resume_file):
                os.remove(self.resume_file)
                print("🗑️ Resume point cleared - scraping completed successfully")
        except Exception as e:
            print(f"Warning: Could not clear resume point: {e}")

    def get_resume_index(self, links):
        """Find the index to resume from in the links list"""
        if not self.last_processed_url:
            return 0

        try:
            # Find the exact URL
            if self.last_processed_url in links:
                index = links.index(self.last_processed_url)
                print(f"🎯 Found resume point at index {index}: {self.last_processed_url}")
                return index + 1  # Start from the next item

            # If exact match not found, try to find a similar URL (in case of slight changes)
            for i, link in enumerate(links):
                if self.last_processed_url.split('/')[-1] in link:  # Match by product slug
                    print(f"🎯 Found similar resume point at index {i}: {link}")
                    return i

        except Exception as e:
            print(f"Warning: Could not find resume index: {e}")

        print("⚠️ Resume point not found in current links, starting from beginning")
        return 0

    vendor = "Ragon House Collection"
    url = "http://ragonhouse.com/"
    home = "http://ragonhouse.com/"
    login = "https://ragonhouse.com/login.php"
    uname = "rick@waresitat.com"
    passw = "ragonhouse1"
    lastStop =  ""
    sitemap = 'https://ragonhouse.com/collections/'
    flag = False
    delay = 1
    counter = 190
    items = []
    links = []

    def export_all_product_urls(self, items):
        with open('./csv/outfile/' + self.vendor + '_product_urls.csv','wb') as ragon_file:
            writer = csv.writer(ragon_file)
            for item in items:
                writer.writerow([item])

    def nextPage(self):        
        try:
            next_button = self.driver.find_element(By.CSS_SELECTOR,"#product-listing-container > nav > ul > li.pagination-item.pagination-item--next > a")
            self.driver.execute_script("arguments[0].click();", next_button)
            self.time.sleep(2)
            return True
        except NoSuchElementException:
            # No more button mean no more pages
            print("No more pages.")
            return False
        except StateElementReferenceException:
            print("No more pages.")
            return False

    def init_login(self,un,pw):
        self.driver.get(self.url)
        self.time.sleep(1)
        # ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#sw_dropdown_2878 > a")).perform()
        # self.time.sleep(1)
        self.driver.find_element(By.XPATH,"/html/body/header/nav/ul/li[3]/a[1]").click()
        self.time.sleep(1)
        # self.driver.find_element(By.CSS_SELECTOR,"#account_info_2878 > div.ty-account-info__buttons.buttons-container > a.cm-dialog-opener.cm-dialog-auto-size.ty-btn.ty-btn__secondary").click()

        # self.time.sleep(1)
        print("Logging in...")
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_email"))).send_keys(un)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(pw)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "login_pass"))).send_keys(Keys.ENTER)
        self.time.sleep(3)
        print("Success.")

    def get_info(self,item=None):
        db = gateway()
        db.name = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > h1").text
        if not db.name:
            return

        db.sku = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > dl.productView-custom > dd").text
        db.cat = "|".join([c.text for c in self.driver.find_elements(By.CSS_SELECTOR,"#main-content > div.container > nav > ol > li.breadcrumb > a > span")])
        try:
            db.desc = self.driver.find_element(By.CSS_SELECTOR,"#tab-description").text
        except:
            db.desc = ""
        try:
            db.stock = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > div.productView-availability > dd").text
        except:
            db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        db.size = self.driver.find_element(By.CSS_SELECTOR,"#main-content > div.container > div > div.productView > section.productView-details.product-data > div > div.productView-dimensions").text
        db.seller = ""
        try:
            db.min1 = self.driver.find_element(By.XPATH,'//*[@id="qty[]"]').get_attribute('value')
        except:
            db.min1 = ""
        try:
            db.price1 = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div[1]/div/div[1]/section[2]/div/div[1]/div[3]/span[3]').text
        except:
            db.price1 = ""
        try:
            db.min2 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > thead > tr > th:nth-child(3)").text.strip("+")
        except:
            db.min2 = ""
        try:
            db.price2 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > tbody > tr > td:nth-child(3) > bdi > span").text
        except:
            db.price2 = ""
        try:
            db.min3 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > thead > tr > th:nth-child(4)").text.strip("+")
        except:
            db.min3 = ""
        try:
            db.price3 = self.driver.find_element(By.CSS_SELECTOR,"div.ty-qty-discount > table > tbody > tr > td:nth-child(4) > bdi > span").text
        except:
            db.price3 = ""
        try:
            db.multi = self.driver.find_element(By.XPATH,'//*[@id="qty[]"]').get_attribute('value')
        except:
            db.multi = ""
        db.dir400 = "Ragon400"
        db.dir160 = "Ragon160"
        #ActionChains(self.driver).move_to_element(self.driver.find_element(By.CSS_SELECTOR,"#fancybox-wrap")).perform()
        #self.time.sleep(1)
        try:
            db.img400 = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div.container > div > div.productView > section.productView-images > figure > div > a"))).get_attribute("href")
        except:
            return
        db.img160 = db.img400.split("/")[-1:][0]
        try:
            db.desc2 = self.driver.find_element(By.CSS_SELECTOR,"#content_description").text
        except:
            db.desc2 = ""
        db.option = ""
        db.dir800 = "Ragon800"
        db.img800 = db.img160
        print(db)
        return db


    def search_item(self,row=None):
        """Search for items.

        Behavior:
        - If `row` is provided, attempt a quick site search using the header search box.
        - If no `row` provided, default to scraping the single collection page
          https://ragonhouse.com/flameless-candles/ (per request).
        Returns a deduplicated list of product page URLs.
        """
        self.items = []

        # If a row/sku is given, try the quick-search box (best-effort).
        if row:
            try:
                print(f"Searching SKU/text: {row}")
                WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#quick-search-expand'))).click()
                self.time.sleep(1)
                q = self.driver.find_element(By.NAME, 'nav-quick-search')
                q.clear()
                q.send_keys(row)
                q.send_keys(Keys.ENTER)
                self.time.sleep(2)
            except Exception as e:
                print('Quick search failed:', e)

        # Default to the single collection page requested by the user
        pages = ['https://ragonhouse.com/flameless-candles/']

        def extract_urls_from_current_page():
            """Scroll to load lazy items and return product links found on the listing."""
            prev_count = 0
            for _ in range(8):  # try a few times to allow lazy loading
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                self.time.sleep(1.5)
                # Try primary selector first, fall back to a common alternative
                elems = self.driver.find_elements(By.XPATH, '//*[@id="product-listing-container"]/div[1]/ul/li/article/div/h3/a')
                if not elems:
                    elems = self.driver.find_elements(By.CSS_SELECTOR, '.card-title a')
                links = [a.get_attribute('href') for a in elems if a.get_attribute('href')]
                if len(links) == prev_count:
                    break
                prev_count = len(links)
            return links

        for page in pages:
            try:
                print('Opening collection page:', page)
                self.driver.get(page)
                self.time.sleep(1)
            except Exception as e:
                print('Failed to load page', page, e)
                continue

            try:
                found = extract_urls_from_current_page()
                if found:
                    self.items.extend(found)
            except Exception as e:
                print('Error extracting URLs from', page, e)

            # Try to paginate (best-effort). If nextPage() finds a next button, gather links there too.
            while True:
                try:
                    has_next = self.nextPage()
                except Exception:
                    has_next = False
                if not has_next:
                    break
                self.time.sleep(1)
                try:
                    found = extract_urls_from_current_page()
                    if found:
                        self.items.extend(found)
                except Exception as e:
                    print('Error extracting after pagination', e)
                    break

        # Deduplicate and return
        return list(dict.fromkeys(self.items))

    def get_links(self):
        """Return product links found on the current listing page."""
        try:
            items = [a.get_attribute("href") for a in self.driver.find_elements(By.XPATH,'//*[@id="product-listing-container"]/div[1]/ul/li/article/div/h3/a')]
        except:
            # fallback selector
            items = [a.get_attribute("href") for a in self.driver.find_elements(By.CSS_SELECTOR, '.card-title a')]
        print(items)
        return items

    def get_all_items(self):
        """Crawl the sitemap/collections, collect product URLs from each collection and paginate."""
        # go to sitemap to read collection links
        try:
            self.driver.get('https://ragonhouse.com/sitemap')
            self.time.sleep(1)
            # the sitemap stores collections in a nested list; target the second list as in search_item
            container = self.driver.find_element(By.CSS_SELECTOR, "#main-content > div.container > ul > li:nth-child(2) > ul")
            cats = [a.get_attribute('href') for a in container.find_elements(By.TAG_NAME, 'a')]
        except Exception:
            # fallback to the collections landing page
            cats = [self.sitemap]

        self.links = []
        for cat in cats:
            print(cat)
            try:
                self.driver.get(cat)
                self.time.sleep(1)
            except Exception:
                continue

            # gather links on the first page
            try:
                self.links.extend(self.get_links())
            except Exception:
                pass

            # paginate and gather more
            while self.nextPage():
                self.time.sleep(1)
                try:
                    self.links.extend(self.get_links())
                except Exception:
                    break

        return list(set(self.links))
