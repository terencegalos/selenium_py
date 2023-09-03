import requests
import random
import time
import concurrent.futures

def get_random_proxy(proxies_list):
    return random.choice(proxies_list)

def fetch_page_with_proxy(url, proxy):
    proxies = {
        "http": proxy,
        "https": proxy
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        return response
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def scrape_with_proxy(url, proxy):
    try:
        response = fetch_page_with_proxy(url, proxy)
        if response and response.status_code == 200:
            print(f"Success! Using proxy: {proxy}")
            print(response.text)
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Error occurred: {e}")

def main():
    url = 'https://example.com'  # Replace this with your target URL
    proxies_list = [
        'http://111.111.111.111:8080',
        'http://222.222.222.222:8080',
        'http://333.333.333.333:8080',
        # Add more proxies here...
    ]
    num_threads = 3  # Number of concurrent threads

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(scrape_with_proxy, url, get_random_proxy(proxies_list)) for _ in range(num_threads)]

        # Wait for all threads to complete
        concurrent.futures.wait(futures)

if __name__ == "__main__":
    main()
