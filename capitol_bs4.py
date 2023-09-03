import requests
import csv
import time
from bs4 import BeautifulSoup

def soup(url):
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html,"lxml")
    return soup

url = "http://www.earthrugs.com/"