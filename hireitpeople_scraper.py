from selenium import webdriver
from selenium.webdriver.common.by import By

import pandas as pd
import time

class Browser:
    def __init__(self,url=None):
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        if url:
            self.browser.get(url)
        else:
            self.browser.get('https://www.hireitpeople.com/resume-database')
        time.sleep(1)

class Scraper(Browser):

    def get_resumes(self):
        return [a.get_attribute("href") for a in self.browser.find_elements(By.CSS_SELECTOR,'.table > tbody:nth-child(1) > tr > td:nth-child(1) > h4:nth-child(1) > a:nth-child(1)')]

    def run(self):
        resume = []
        
        inp = input('Enter the category: ')
        pagenum = input('Enter the page range to scrape: ')
        self.browser.get(inp)
        time.sleep(1)
        
        resumes = self.get_resumes()
        for resume in resumes:
            br = Browser(resume)
            resumes.append(Resume(br))
            br.browser.close()


        resume_exporter(resumes)


def resume_exporter(data):
    df = pd.DataFrame(data)
    df.to_excel('hireitresumes.xlsx',index=False)





class Resume:
    def __init__(self,br):
        self.name = br.browser.find_element(By.XPATH,'/html/body/div[3]/section[2]/div/div/div/div[1]/div[1]/div[1]/div/h3').text
        self.summary = [line.text for line in br.browser.find_elements(By.CSS_SELECTOR,'.single-post-body > ul:nth-child(3) > li')]
        
        skills_dirty = [line.text for line in br.browser.find_elements(By.XPATH,'/html/body/div[3]/section[2]/div/div/div/div[1]/div[2]/p')]
        
        skills = []
        flag = False
        for line in skills_dirty:
            if 'professional experience' in line.lower():
                flag == True

            if flag == True:
                continue

            skills.append(line)

        self.skills = skills

        self.__str__()
    
    def __str__(self):
        print(f'{self.name,self.summary,self.skills}')
            


if __name__ == '__main__':
    scraper = Scraper()
    scraper.run()