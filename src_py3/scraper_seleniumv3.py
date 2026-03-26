import sys
import csv
import os
import time
import importlib.util
from datetime import datetime
from tqdm import tqdm

# Custom modules
from helper.active_record import ActiveRecord
import helper.webdriver_config as webdriver_config
from helper import config

class Scraper:
    """
    Consolidated Scraper class handling both targeted (missing items) 
    and sitewide scraping modes.
    """
    def __init__(self, vendor_name, scraping_mode=None):
        self.browser = webdriver_config.init_driver()
        self.vendor_name = vendor_name
        self.mode = scraping_mode
        self.delay = 1
        
        # Dynamically load vendor-specific class
        self.target_vendor = self._load_vendor_class(vendor_name)
        
        # Initialize scraping targets based on mode
        self.links = []
        if self.mode and 'sitewide' in self.mode:
            print(f"🚀 Starting sitewide scraping for {vendor_name}...")
            self.target_vendor.get_all_items()
            self.links = self.target_vendor.links
        else:
            print(f"🔍 Starting targeted scraping for {vendor_name} (missing items)...")
            self.missing = self.target_vendor.get_missing(self.target_vendor.vendor)
            self.total_missing = len(self.missing)

        self.active_record = ActiveRecord()

    def _load_vendor_class(self, vendor_name):
        """Helper to resolve and instantiate the vendor class."""
        vendor_class_filename = f"{vendor_name}_class"
        vendor_module_path = os.path.join(os.path.dirname(__file__), "vendor", f"{vendor_class_filename}.py")
        
        if not os.path.exists(vendor_module_path):
            raise FileNotFoundError(f"Vendor module not found: {vendor_module_path}")

        spec = importlib.util.spec_from_file_location(vendor_class_filename, vendor_module_path)
        vendor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(vendor_module)
        
        vendor_class = getattr(vendor_module, vendor_name)
        return vendor_class(self.browser, self.mode)

    def run(self):
        # Setup fail-safe backup file using path from central config
        backup_filename = f"{self.target_vendor.vendor}_output_fail_safe.csv"
        backup_path = os.path.join(config.CSV_OUTFILE_PATH, backup_filename)
        
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        with open(backup_path, "w", encoding="utf-8", newline="") as backup_file:
            writer = csv.writer(backup_file)

            # 1. Collect links if in targeted mode
            if not self.mode or 'sitewide' not in self.mode:
                for sku in tqdm(self.missing, desc="Searching SKUs"):
                    # self.counter.subtotal += 1.0
                    # print("Progress: {}%".format(int((self.counter.subtotal / self.total) * 100)))

                    items = self.target_vendor.search_item(sku)
                    if items:
                        self.links.extend(items)

            # 2. Process collected links
            if self.target_vendor.results(self.links):
                self._process_links(writer)
            else:
                # Fallback for single item or direct navigation
                print("\n⚠️ No multiple links found, attempting direct info extraction...")
                self._extract_and_save(writer)

        # 3. Finalize and export
        self._finalize()

    def _process_links(self, writer):
        """Iterates through links and handles resume logic."""
        resume_index = 0
        if self.mode and 'sitewide' in self.mode and hasattr(self.target_vendor, 'get_resume_index'):
            resume_index = self.target_vendor.get_resume_index(self.links)
            print(f"▶️ Resuming from index: {resume_index}")

        successful_count = 0
        pbar = tqdm(self.links[resume_index:], initial=resume_index, total=len(self.links), desc="Scraping Products")
        
        for item in pbar:
            if hasattr(self.target_vendor, 'is_valid_product_url') and not self.target_vendor.is_valid_product_url(item):
                continue
            
            try:
                self.target_vendor.navigate(item)
                self._extract_and_save(writer)
                successful_count += 1
                
                if hasattr(self.target_vendor, 'save_resume_point'):
                    self.target_vendor.save_resume_point(item)
                    
            except Exception as e:
                print(f"\n❌ Error on {item}: {e}")
                continue

        if hasattr(self.target_vendor, 'clear_resume_point'):
            self.target_vendor.clear_resume_point()
        
        print(f"\n✅ Finished! Processed {successful_count} items.")

    def _extract_and_save(self, writer):
        """Extraction logic shared between modes."""
        db_entries = self.target_vendor.get_info()
        time.sleep(self.delay)

        if db_entries:
            entries = db_entries if isinstance(db_entries, list) else [db_entries]
            for entry in entries:
                if entry:
                    self.active_record.save(entry)
                    writer.writerow(entry.retrieve())

    def _finalize(self):
        """Export to final file and cleanup."""
        time.sleep(2)
        print(f"📦 Exporting results for {self.target_vendor.vendor}...")
        self.target_vendor.send_to_file(self.target_vendor.vendor, self.active_record)
        print(f"📅 Finished at: {datetime.now()}")
        self.browser.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scraper_seleniumv3.py <vendor_name> [mode]")
        sys.exit(1)
        
    v_name = sys.argv[1]
    v_mode = sys.argv[2] if len(sys.argv) > 2 else None
    
    scraper = Scraper(v_name, v_mode)
    scraper.run()


        # Close the backup file and wait before sending to database
        backup_file.close()
        time.sleep(3)

        # Send scraped data to file and close the browser
        self.target_vendor.send_to_file(self.target_vendor.vendor, self.active_record)
        print("Execution finished at: {}".format(datetime.now()))
        self.target_vendor.driver.quit()


if __name__ == "__main__":
    vendor_name = sys.argv[1]
    mode = sys.argv[2]
    scraper = Scraper(vendor_name,mode)
    scraper.run()
    # os.system('shutdown -s') # shutdown down the computer
