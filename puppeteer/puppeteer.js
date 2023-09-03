const puppeteer = require('puppeteer');

class Browser {
  constructor(url) {
    this.delay = 5000;
    this.url = url;
  }

  async init() {
    this.browser = await puppeteer.launch({ headless: true });
    this.page = await this.browser.newPage();
    await this.page.goto(this.url, { waitUntil: 'load' });
    await this.page.setViewport({ width: 1920, height: 1080 });
  }
}

class Scraper extends Browser {
  constructor(url) {
    super(url);
    this.results = [];
    this.counter = 0;
    this.final = [];
  }

  async get_all_designers_by_zip(zip) {
    await this.search_zip(zip);
    const page_results = await this.grab_page_designers();
    this.results = this.results.concat(page_results);

    while (await this.is_next_page_available()) {
      try {
        const page_results = await this.grab_page_designers();
        this.results = this.results.concat(page_results);
      } catch {
        console.log('End of pages reached.');
        break;
      }
    }

    return this.results;
  }

  async search_zip(zip) {
    await this.page.waitForSelector('.pro-location-autosuggest__input');
    try {
      await this.page.click(
        '#hz-page-content-wrapper > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(4) > span:nth-child(1) > a:nth-child(1)'
      );
      await this.page.waitForTimeout(this.delay);
    } catch {
      console.log('');
    }

    try {
      await this.page.waitForSelector('.pro-location-autosuggest__input');
    } catch {
      await this.page.waitForSelector('#hui-text-input-1');
    }

    await this.page.click('.pro-location-autosuggest__input');
    await this.page.keyboard.type(zip);
    await this.page.keyboard.press('Enter');
    await this.page.waitForTimeout(this.delay);
  }

  async grab_page_designers() {
    const links = await this.page.$$eval(
      'li.hz-pro-search-results__item > div:nth-child(1) > a:nth-child(1)',
      (links) => links.map((a) => a.href)
    );
    return links;
  }

  async is_next_page_available() {
    if (this.counter > 2) {
      return false;
    }
    try {
      await this.page.click(
        'div.directory-results-pagination:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > a:nth-child(10) > span:nth-child(1) > span:nth-child(1)'
      );
    } catch {
      await this.page.click('a.hz-pagination-link:nth-child(11)');
    }
    console.log('Navigating page..');
    await this.page.waitForTimeout(this.delay);
    this.counter += 1;
    return true;
  }

  async scrape_sites_built_by_houzz(results, keyword) {
    for (const res of results) {
      await this.page.goto(res, { waitUntil: 'load' });
      await this.page.waitForTimeout(this.delay);

      try {
        const link = await this.page.$eval(
          '#business > div:nth-child(2) > div:nth-child(3) > p:nth-child(2) > a:nth-child(1) > div:nth-child(1) > span:nth-child(1)',
          (el) => el.innerText.trim()
        );
       
