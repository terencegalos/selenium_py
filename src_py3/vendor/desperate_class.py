from helper.table_gateway import gateway
from helper.domainobject import domainobject
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class desperate(domainobject):

    def __init__(self, driver, scraper_mode):
        super().__init__(driver)
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

    vendor = "Desperate Tin Signs"
    url = "http://www.desperate.com/shophome.cfm"
    home = "http://www.desperate.com/shophome.cfm"
    login_url = "https://desperate.com/login.php"
    uname = "service@waresitat.com"
    passw = "wolfvill1"
    delay = 1
    links = []
        
    def init_login(self, un, pw):
        # Navigate to login page first
        self.driver.get(self.login_url)
        self.time.sleep(1)

        print("Logging in...")
        try:
            # Find login fields by name (simplified approach)
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "login_email"))
            )
            password_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "login_pass"))
            )

            # Fill and submit login form
            email_field.clear()
            email_field.send_keys(un)
            password_field.clear()
            password_field.send_keys(pw)
            password_field.send_keys(Keys.ENTER)
            self.time.sleep(3)
            print("Success.")

        except Exception as e:
            print(f"Login failed: {e}")
            print("Continuing without login...")

    def get_info(self, item=None):
        db = gateway()
        print(f"Getting item info: {self.driver.current_url}")
        
        try:
            # Product name
            db.name = self.driver.find_element(By.CSS_SELECTOR, "#product-page-with-sidenav > div.product-schema > div.productView > section > div > h1").text
        except NoSuchElementException:
            print("Error: Product name not found")
            db.name = ""
        
        try:
            # SKU
            db.sku = self.driver.find_element(By.CSS_SELECTOR, "#product-page-with-sidenav > div.product-schema > div.productView > section > div > div > dl > dd").text
        except NoSuchElementException:
            print("Error: SKU not found")
            db.sku = ""
        
        try:
            # Category - try primary method first
            db.cat = self.driver.find_element(By.CSS_SELECTOR, "#product-page-with-sidenav > div.product-schema > div.productView > section > div > h2 > a > span").text
        except NoSuchElementException:
            try:
                # Fallback to breadcrumb navigation
                breadcrumbs = self.driver.find_elements(By.CSS_SELECTOR, "#product-page-with-sidenav > div.product-schema > ul > li.breadcrumb > a")
                db.cat = "|".join([bread.text for bread in breadcrumbs])
            except:
                db.cat = ""
        
        try:
            # Description - try specific paragraph first
            db.desc = self.driver.find_element(By.CSS_SELECTOR, "#tab-description > p:nth-child(2)").text
        except NoSuchElementException:
            try:
                # Fallback to entire description tab
                db.desc = self.driver.find_element(By.CSS_SELECTOR, "#tab-description").text
            except:
                db.desc = ""
        
        db.stock = ""
        db.sale = ""
        db.set = ""
        db.custom = ""
        
        try:
            # Size from description
            desc_text = self.driver.find_element(By.CSS_SELECTOR, "#tab-description > p:nth-child(2)").text
            lines = desc_text.splitlines()
            db.size = lines[2] if len(lines) > 2 else ""
        except:
            db.size = ""
        
        db.seller = ""
        db.min1 = 1
        
        try:
            # Price
            db.price1 = self.driver.find_element(By.CSS_SELECTOR, "#product-page-with-sidenav > div.product-schema > div.productView > section > div > div > div.price-section > span.price").text
        except NoSuchElementException:
            try:
                # Alternative price selector
                db.price1 = self.driver.find_element(By.CSS_SELECTOR, "span.price--withoutTax").text
            except:
                db.price1 = ""
        
        db.min2 = ""
        db.price2 = ""
        db.min3 = ""
        db.price3 = ""
        db.multi = 1
        db.dir400 = "desperate400"
        db.dir160 = "desperate160"
        
        try:
            # Product image
            img_element = self.driver.find_element(By.CSS_SELECTOR, "#product-images-container > div.main-image-container img")
            db.img400 = img_element.get_attribute("src")
            if not db.img400:
                # Try data-src attribute if src is empty
                db.img400 = img_element.get_attribute("data-src")
        except NoSuchElementException:
            try:
                # Alternative image selector
                img_element = self.driver.find_element(By.CSS_SELECTOR, ".productImageSlider img")
                db.img400 = img_element.get_attribute("src") or img_element.get_attribute("data-src")
            except:
                print("Warning: Image not detected.")
                db.img400 = ""
                return None
        
        if db.img400:
            db.img160 = db.img400.split("/")[-1]
        else:
            db.img160 = ""
            
        db.desc2 = ""
        db.option = ""
        db.dir800 = "desperate800"
        db.img800 = db.img160
        
        print(db)
        return db
        
        
    def search_item(self, row):
        print(f"\nSearching for item: {row}\n")
        
        while True:
            try:
                search_input = self.driver.find_element(By.NAME, "search_query")
                search_input.clear()
                search_input.send_keys(str(row))
                search_input.send_keys(Keys.ENTER)
                self.time.sleep(2)
                break
            except NoSuchElementException:
                print("Search box not found, refreshing page...")
                self.driver.refresh()
                self.time.sleep(1)
                continue

        try:
            # Scroll down to load results
            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
            self.time.sleep(1)
            
            # Try to find first product result
            product_link = self.driver.find_element(By.CSS_SELECTOR, "#product-listing-container > form.both-grid-default > ul > ul > li:nth-child(1) > article > div > h4 > a")
            item_url = product_link.get_attribute("href")
            print(f"Found item: {item_url}")
            return [item_url]
        except NoSuchElementException:
            try:
                # Alternative selector for product results
                product_link = self.driver.find_element(By.CSS_SELECTOR, ".productGrid li:first-child article h4 a")
                item_url = product_link.get_attribute("href")
                print(f"Found item: {item_url}")
                return [item_url]
            except:
                print(f"No results found for SKU: {row}")
                return None
    
    def get_categories(self):
        """Get all category links from the Tin Signs section"""
        try:
            # Navigate to home page
            self.driver.get(self.home)
            self.time.sleep(2)
            
            print("Expanding Tin Signs category...")
            # Click "+ Tin Signs" to expand subcategories
            try:
                tin_signs_link = self.driver.find_element(By.LINK_TEXT, "+ Tin Signs")
                tin_signs_link.click()
                self.time.sleep(2)
            except NoSuchElementException:
                # Try alternative selector
                tin_signs_link = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Tin Signs")
                tin_signs_link.click()
                self.time.sleep(2)
            
            # Get all subcategory links (those starting with "+")
            category_elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "+")
            categories = []
            
            for cat_element in category_elements:
                href = cat_element.get_attribute("href")
                text = cat_element.text
                if href and "shophome.cfm" in href:
                    categories.append(href)
                    print(f"Found category: {text} - {href}")
            
            print(f"Total categories found: {len(categories)}")
            return categories
            
        except Exception as e:
            print(f"Error getting categories: {e}")
            return []
    
    def get_items_from_page(self):
        """Extract all product links from current page"""
        try:
            # Wait for products to load
            self.time.sleep(2)

            # Find all product links - different selectors for /all/ page vs category pages
            product_links = []

            # Check if we're on the /all/ page or a category page
            current_url = self.driver.current_url
            if "/all/" in current_url:
                # Selectors for /all/ page
                selectors = [
                    ".product a[href*='/']",  # Product containers with links
                    "article a[href*='/']",   # Article containers with links
                    ".card a[href*='/']"      # Card containers with links
                ]
            else:
                # Original selectors for category pages
                selectors = [
                    "table tbody tr td a[href*='productdetails']",
                    "a[href*='productdetails']",
                    ".product-link",
                    "table a"
                ]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute("href")
                        # Comprehensive filtering for valid product URLs only
                        if (href and
                            href.startswith("https://desperate.com/") and
                            not href.endswith("/all/") and
                            not "#0" in href and
                            not href.endswith("#") and
                            "/all/?page=" not in href and
                            "cart.php" not in href and  # Exclude cart URLs
                            "login.php" not in href and  # Exclude login URLs
                            "shophome.cfm" not in href and  # Exclude category pages
                            "search.php" not in href and  # Exclude search pages
                            href not in product_links and  # Avoid duplicates within page
                            len(href.split('/')) >= 4):  # Must have at least domain + path segments
                            product_links.append(href)

                    if product_links:
                        print(f"Found {len(product_links)} products on this page using selector: {selector}")
                        break
                except:
                    continue

            return product_links

        except Exception as e:
            print(f"Error getting items from page: {e}")
            return []
    
    def has_next_page(self):
        """Check if there's a next page and navigate to it"""
        try:
            # Look for the specific pagination structure for desperate.com
            next_button = self.driver.find_element(By.CSS_SELECTOR, "li.pagination-item--next a.pagination-link")
            next_url = next_button.get_attribute("href")
            
            if next_url and "page=" in next_url:
                print(f"Found next page: {next_url}")
                self.driver.get(next_url)
                self.time.sleep(2)
                return True
            
            return False
            
        except:
            return False
    
    def is_valid_product_url(self, url):
        """Validate if URL is a legitimate product page"""
        if not url or not isinstance(url, str):
            return False

        # Basic URL structure checks
        if not url.startswith("https://desperate.com/"):
            return False

        # Exclude non-product URLs
        exclude_patterns = [
            "cart.php",
            "login.php",
            "shophome.cfm",
            "search.php",
            "/all/",
            "?page=",
            "#"
        ]

        for pattern in exclude_patterns:
            if pattern in url:
                return False

        # Must have proper product URL structure (domain + product-slug)
        parts = url.replace("https://", "").split("/")
        if len(parts) < 2 or not parts[1]:  # Must have at least domain + product path
            return False

        return True

    def get_all_items(self):
        """Scrape all product URLs using direct pagination"""
        print("Starting sitewide scraping for Desperate Tin Signs...")

        # Resume point is already loaded in constructor

        # Start with the first page
        base_url = "https://desperate.com/all/?page="
        page_num = 1
        current_url = f"{base_url}{page_num}"

        try:
            self.driver.get(current_url)
            self.time.sleep(2)

            # Get products from first page
            page_items = self.get_items_from_page()
            self.links.extend(page_items)
            print(f"Page {page_num}: Found {len(page_items)} products")

            # Paginate through all pages
            while self.has_next_page():
                page_num += 1
                print(f"Processing page {page_num}...")

                # Get products from current page
                page_items = self.get_items_from_page()
                self.links.extend(page_items)
                print(f"Page {page_num}: Found {len(page_items)} products")

        except Exception as e:
            print(f"Error during sitewide scraping: {e}")

        # Comprehensive deduplication and filtering
        print(f"\nBefore deduplication: {len(self.links)} total links found")

        # Remove duplicates
        unique_links = list(set(self.links))
        print(f"After removing duplicates: {len(unique_links)} unique links")

        # Additional filtering to ensure only valid product URLs
        valid_product_links = []
        for link in unique_links:
            if self.is_valid_product_url(link):
                valid_product_links.append(link)

        self.links = valid_product_links
        print(f"✓ After filtering invalid URLs: {len(self.links)} valid product links")

        # If resuming, find the resume index
        resume_index = 0
        if resume_url:
            resume_index = self.get_resume_index(self.links)
            if resume_index > 0:
                print(f"▶️ Resuming from index {resume_index} (after: {resume_url})")

        print(f"✓ Total unique products found: {len(self.links)}")
        print(f"✓ Will start processing from index: {resume_index}")
        return self.links

