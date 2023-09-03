from tkinter import *
from selenium import webdriver

# Class to perform Amazon scraping and display results in a tkinter GUI
class AmazonScraper:
    # Initialize the GUI
    def __init__(self, master):
        self.master = master
        master.title("Amazon Scraper")

        # Create GUI elements
        self.label_search = Label(master, text="Search:")
        self.entry_search = Entry(master)
        self.btn_search = Button(master, text="Search", command=self._search)

        self.label_results = Label(master, text="Results:")

        self.text_results = Text(master, height=30, width=100)
        self.scroll_results = Scrollbar(master, command=self.text_results.yview)
        self.text_results.config(yscrollcommand=self.scroll_results.set)

        # Pack GUI elements
        self.label_search.pack()
        self.entry_search.pack()
        self.btn_search.pack()

        self.label_results.pack()
        self.text_results.pack(side=LEFT, fill=Y)
        self.scroll_results.pack(side=RIGHT, fill=Y)

        # Initialize Selenium browser driver
        self.driver = webdriver.Chrome() # or other browser driver

    # Function to handle search button click event
    def _search(self):
        # Get search query from entry field
        search_query = self.entry_search.get()

        # Construct URL for Amazon search results page
        url = "https://www.amazon.com/s?k=" + search_query.replace(" ", "+")

        # Open the URL in the browser
        self.driver.get(url)

        # TODO: Scrape data from the search results page and display it in the GUI
        # Example:
        # results = self.driver.find_elements_by_class_name("s-result-item")
        # for result in results:
        #     title = result.find_element_by_class_name("a-text-normal").text
        #     price = result.find_element_by_class_name("a-offscreen").text
        #     self.text_results.insert(END, title + " - " + price + "\n")

    # Cleanup function to quit the browser driver
    def __del__(self):
        self.driver.quit()

# Main function
if __name__ == '__main__':
    # Create the tkinter window and AmazonScraper instance
    root = Tk()
    scraper = AmazonScraper(root)
    root.mainloop()
