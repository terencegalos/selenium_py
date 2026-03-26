#!/usr/bin/env python3
"""
Test script to demonstrate resume functionality for desperate.com scraper
"""

import os
import sys
sys.path.append('.')

from vendor.desperate_class import desperate

def test_resume_functionality():
    """Test the resume functionality without actually scraping"""

    print("🧪 Testing Resume Functionality for Desperate.com Scraper")
    print("=" * 60)

    # Create a mock vendor instance (without browser for testing)
    class MockDesperate:
        def __init__(self):
            self.vendor = "Desperate Tin Signs"
            self.resume_file = os.path.join(os.path.dirname(__file__), "resume", f"{self.vendor.replace('/', '_')}_resume.txt")
            self.last_processed_url = None
            self._ensure_resume_directory()

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

    # Test the functionality
    vendor = MockDesperate()

    # Sample URLs that would be collected
    sample_links = [
        "https://desperate.com/sticker-bouncy-castle-set-of-6/",
        "https://desperate.com/magnet-smith-wesson-round/",
        "https://desperate.com/america-let-freedom-reign/",
        "https://desperate.com/view-all/10-x-10-mdf-bills-gnome-sign/",  # This is our resume point
        "https://desperate.com/dads-repair-service/",
        "https://desperate.com/superman-retro-panels/",
        "https://desperate.com/chevy-parts-pistons/"
    ]

    print("\n📋 Sample product links:")
    for i, link in enumerate(sample_links):
        print(f"  {i}: {link}")

    print("\n1️⃣ Testing resume point saving...")
    resume_url = "https://desperate.com/view-all/10-x-10-mdf-bills-gnome-sign/"
    vendor.save_resume_point(resume_url)

    print("\n2️⃣ Testing resume point loading...")
    loaded_url = vendor.load_resume_point()

    print("\n3️⃣ Testing resume index finding...")
    resume_index = vendor.get_resume_index(sample_links)

    print("\n📊 Resume Test Results:")
    print(f"   Resume URL: {resume_url}")
    print(f"   Resume Index: {resume_index}")
    print(f"   Items to process: {sample_links[resume_index:]}")
    print(f"   Items remaining: {len(sample_links) - resume_index}")

    print("\n4️⃣ Testing resume point clearing...")
    vendor.clear_resume_point()

    print("\n✅ Resume functionality test completed!")
    print("\n💡 How it works:")
    print("   - When scraping is interrupted, the last successfully processed URL is saved")
    print("   - On restart, the scraper finds this URL in the links list and resumes from the next item")
    print("   - This prevents reprocessing already completed items")
    print("   - Resume point is cleared when scraping completes successfully")

if __name__ == "__main__":
    test_resume_functionality()