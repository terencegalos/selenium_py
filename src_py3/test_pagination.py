#!/usr/bin/env python3
"""
Test the new pagination approach for desperate.com
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Import the desperate class
from vendor.desperate_class import desperate

def test_pagination():
    """Test the new pagination approach"""

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    scraper = desperate(driver, "sitewide")

    try:
        print("Testing new pagination approach...")

        # Test the first page
        print("Loading first page: https://desperate.com/all/?page=1")
        driver.get("https://desperate.com/all/?page=1")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Check if pagination exists
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.pagination-item--next a.pagination-link")
            next_url = next_button.get_attribute("href")
            print(f"✅ Found next button with URL: {next_url}")
        except:
            print("❌ Next button not found")

        # Test product extraction
        product_links = scraper.get_items_from_page()
        print(f"✅ Found {len(product_links)} products on first page")

        if product_links:
            print(f"Sample product URLs:")
            for i, link in enumerate(product_links[:3]):
                print(f"  {i+1}. {link}")

        # Test has_next_page method
        has_next = scraper.has_next_page()
        print(f"✅ has_next_page() returned: {has_next}")

        print("🎉 Pagination test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

    finally:
        driver.quit()

if __name__ == "__main__":
    success = test_pagination()
    sys.exit(0 if success else 1)