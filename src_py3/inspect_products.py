#!/usr/bin/env python3
"""
Inspect the product structure on desperate.com/all/ page
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def inspect_products():
    """Inspect product elements on the /all/ page"""

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print("Inspecting product structure on /all/ page...")
        driver.get("https://desperate.com/all/?page=1")

        # Look for common product link patterns
        selectors_to_try = [
            "a[href*='productdetails']",
            ".product-item a",
            ".productCard a",
            ".product a",
            "article a",
            ".card a",
            "[data-product-link]",
            "a[href*='/products/']"
        ]

        print("\n=== TESTING PRODUCT SELECTORS ===")
        for selector in selectors_to_try:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✅ {selector}: Found {len(elements)} elements")
                    # Show first few hrefs
                    for i, elem in enumerate(elements[:3]):
                        href = elem.get_attribute("href")
                        if href:
                            print(f"    {i+1}. {href}")
                    print()
                else:
                    print(f"❌ {selector}: No elements found")
            except Exception as e:
                print(f"❌ {selector}: Error - {e}")

        # Look for product containers
        print("\n=== LOOKING FOR PRODUCT CONTAINERS ===")
        container_selectors = [
            ".product-item",
            ".productCard",
            ".product",
            "article",
            ".card",
            "[data-product]"
        ]

        for selector in container_selectors:
            try:
                containers = driver.find_elements(By.CSS_SELECTOR, selector)
                if containers:
                    print(f"✅ {selector}: Found {len(containers)} containers")
                    # Check if containers have links
                    for i, container in enumerate(containers[:2]):
                        links = container.find_elements(By.TAG_NAME, "a")
                        if links:
                            href = links[0].get_attribute("href")
                            print(f"    Container {i+1} has link: {href}")
                else:
                    print(f"❌ {selector}: No containers found")
            except Exception as e:
                print(f"❌ {selector}: Error - {e}")

    except Exception as e:
        print(f"Error during inspection: {e}")

    finally:
        driver.quit()

if __name__ == "__main__":
    inspect_products()