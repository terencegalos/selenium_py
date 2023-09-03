import time
import threading
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up Selenium web driver
driver = webdriver.Chrome()

# Define the URLs to scrape
urls = [
    'https://example.com/page1',
    'https://example.com/page2',
    'https://example.com/page3',
    'https://example.com/page4',
    'https://example.com/page5'
]

# Set up MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="mydatabase"
)

# Define a function to store data in MySQL
def store_data(data):
    cursor = mydb.cursor()
    sql = "INSERT INTO mytable (data) VALUES (%s)"
    cursor.execute(sql, (data,))
    mydb.commit()

# Define a function to scrape a single URL
def scrape_url(url):
    # Navigate to the URL and wait for the page to load
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    # Get the page source and create a BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Extract the data you need from the soup object
    data = soup.find_all('div', {'class': 'my-data'})
    
    # Store the data in MySQL
    for d in data:
        store_data(str(d))
    
    # Print a message to indicate that the scraping is complete for this URL
    print(f'Scraping complete for {url}')
    
# Define a function to scrape all URLs in parallel
def scrape_urls(urls):
    # Create a thread for each URL
    threads = []
    for url in urls:
        thread = threading.Thread(target=scrape_url, args=(url,))
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Call the scrape_urls function to start the scraping process
scrape_urls(urls)

# Close the MySQL connection and the Selenium web driver
mydb.close()
driver.quit()
