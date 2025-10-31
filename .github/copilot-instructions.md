# Selenium Web Scraper Codebase Instructions

## Architecture Overview

This is a multi-vendor e-commerce product scraping system with vendor-specific scrapers. The core architecture follows an object-oriented pattern with:

- **Main Scraper**: `src_py3/scraper_seleniumv3.py` - Entry point that dynamically loads vendor classes
- **Vendor Classes**: `src_py3/vendor/*_class.py` - Individual scrapers inheriting from `domainobject`
- **Helper Framework**: `src_py3/helper/` - Core abstractions and utilities
- **Data Output**: CSV files in `src_py3/helper/csv/outfile/`

## Key Components

### Vendor Class Pattern
All vendor scrapers inherit from `helper.domainobject.domainobject` and follow this structure:
```python
class vendor_name(domainobject):
    vendor = "Vendor Display Name"
    url = "https://vendor-website.com"
    uname = "login_email"
    passw = "password"
    delay = 1
    links = []  # Product URLs to scrape
```

Required methods:
- `init_login(un, pw)` - Handle vendor-specific login flow
- `get_info()` - Extract product data, returns `table_gateway.gateway` object
- `search_item(sku)` - Find product URLs by SKU

### Data Model
Product data uses `helper.table_gateway.gateway` with standardized fields:
```
name, sku, cat, desc, stock, sale, set, custom, size, seller,
min1, price1, min2, price2, min3, price3, multi,
dir400, dir160, img400, img160, desc2, option, dir800, img800
```

### Running Scrapers
Execute via command line with vendor name and mode:
```bash
python src_py3/scraper_seleniumv3.py vendor_name scraping_mode
```

Example vendor names: `capitol`, `hannas`, `ragon`, `janmichael`
Modes: `sitewide` (scrape all products) or missing items from CSV

## WebDriver Configuration

Uses `undetected-chromedriver` with anti-detection measures. Configure in `helper/webdriver_config.py`:
- Prompts for headless mode on startup
- Includes stealth options and user agent spoofing
- Maximizes window and clears cookies

## Data Flow

1. **Input**: Missing SKUs read from `helper/csv/outfile/noimg/{vendor}.csv`
2. **Search**: Vendor-specific search by SKU via `search_item()`
3. **Scrape**: Navigate to product pages, extract data via `get_info()`
4. **Storage**: Save to `ActiveRecord` container and backup CSV
5. **Output**: Final CSV at `helper/csv/outfile/{vendor} output.csv`

## File Organization

- `src_py3/` - Main codebase (Python 3)
- Root directory - Legacy Python 2 scripts (deprecated)
- `vendor/` - Numbered catalog files (`7898_catalog.py`) for bulk data processing
- `xls/` - Excel file processing utilities

## Development Patterns

### Error Handling
Scrapers include extensive retry logic and backup mechanisms:
- Failed items saved to `*_output_fail_safe.csv`
- Progress tracking with `tqdm`
- Manual CAPTCHA handling prompts

### Anti-Detection
- Random delays between actions
- Character-by-character password entry with random timing
- Smooth scrolling simulation
- User agent rotation

### Vendor-Specific Adaptations
Each vendor class handles site-specific challenges:
- Different login flows (`capitol_class.py` has complex scrolling/CAPTCHA)
- Varying product page structures
- Option/variant handling for products with multiple sizes/colors

## Testing & Debugging

- Use `test.bat` for batch processing multiple vendors
- Check `debug.log` and `geckodriver.log` for browser issues
- Backup files serve as recovery points during development
- Progress bars show real-time scraping status

## Dependencies

Key packages in `requirements.txt`:
- `selenium==4.28.1` - Web automation
- `undetected-chromedriver==3.5.5` - Anti-detection
- `beautifulsoup4==4.12.2` - HTML parsing fallback
- `tqdm==4.66.1` - Progress bars
- `openpyxl==3.1.2` - Excel file handling

Run scrapers from `src_py3/` directory to ensure proper module imports.