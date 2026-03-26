# Selenium Web Scraper Codebase Instructions

## Architecture Overview

This is a comprehensive **multi-vendor e-commerce product scraping and catalog management system** with vendor-specific scrapers and a centralized data synchronization framework. The system processes 69+ vendors with 512K+ lines of code, handling web scraping, data consolidation, and business-ready Excel outputs.

### Core Architecture Components

- **Main Scraper**: `src_py3/scraper_seleniumv3.py` - Entry point with dynamic vendor loading and resume functionality
- **Vendor Classes**: `src_py3/vendor/*_class.py` - Individual scrapers inheriting from `domainobject`
- **Catalog Classes**: `src_py3/vendor/*_catalog.py` - Bulk data processing for existing vendor catalogs
- **Data Synchronization**: `src_py3/update_waresitat.py` - Master catalog management and vendor data consolidation
- **Helper Framework**: `src_py3/helper/` - Core abstractions, data models, and utilities
- **Data Output**: CSV files in `src_py3/helper/csv/outfile/` and Excel files in `src_py3/xls/output/`

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

### Catalog Class Pattern (Bulk Data Processing)
Bulk data processing classes for existing vendor catalogs:

#### **Two Types of Catalog Classes:**

1. **Excel-Based Catalogs** (Traditional vendor data files)
2. **CSV-Based Catalogs** (Processed scraped data)

#### **Excel-Based Catalog Pattern:**
```python
from helper.xls_getter import TableData
import datetime, xlrd

class Vendor_Name():
    prod = {}  # Product dictionary
    skus = None  # SKU list
    disc = False  # Discontinued flag

    def __init__(self, vendor, mode=2):
        table = TableData(vendor, mode)  # Loads from xls/{vendor.code}.xls
        rsheet = table.getSheet()

        for x in range(1, rsheet.nrows):
            # Process Excel rows into product format
            # ... vendor-specific logic ...
```

#### **CSV-Based Catalog Pattern:**
```python
import csv
import os

class Vendor_Name():
    prod = {}
    skus = None
    disc = False

    def is_num(self, num):
        try:
            float(num)
            return True
        except:
            return False

    def __init__(self, vendor, mode=2):
        # Path to scraped CSV data
        csv_path = os.path.join(os.path.dirname(__file__), "..", "helper", "csv", "outfile", f"{vendor.name} output.csv")

        if not os.path.exists(csv_path):
            print(f"Warning: CSV file not found at {csv_path}")
            self._initialize_skus()
            return

        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            for row_num, row in enumerate(reader, 1):
                try:
                    if not row or len(row) < 2:
                        continue

                    # Map CSV columns to standard product schema
                    # CSV: name,sku,cat,desc,stock,sale,set,custom,size,seller,min1,price1,min2,price2,min3,price3,multi,dir400,dir160,img400,img160,desc2,option,dir800,img800
                    if len(row) >= 25:
                        name, sku, cat, desc, stock, sale, set_val, custom, size, seller, \
                        min1, price1, min2, price2, min3, price3, multi, \
                        dir400, dir160, img400, img160, desc2, option, dir800, img800 = row[:25]

                        # Data validation and cleaning
                        if not sku:
                            continue

                        # Clean price data
                        if price1 and price1.startswith('$'):
                            price1 = price1[1:]

                        # Convert numeric fields
                        if self.is_num(price1):
                            price1 = round(float(price1), 2)

                        # Create product entry with standard schema
                        self.prod[sku] = {
                            'name': name, 'sku': sku, 'cat': cat, 'desc': desc,
                            'stock': stock, 'sale': sale, 'set': set_val, 'custom': custom,
                            'size': size, 'top': '', 'min': min1, 'price1': price1,
                            'min2': min2, 'price2': price2, 'min3': min3, 'price3': price3,
                            'multi': multi, 'img400': img400, 'img160': img160,
                            'jpg400': img400.split('/')[-1] if img400 and '/' in img400 else img400,
                            'jpg160': img160.split('/')[-1] if img160 and '/' in img160 else img160,
                            'desc2': desc2, 'opt': option, 'img800': img800,
                            'jpg800': img800.split('/')[-1] if img800 and '/' in img800 else img800,
                            'isUpdateAvailable': ''
                        }

                except Exception as e:
                    print(f"Warning: Error processing row {row_num}: {e}")
                    continue

        self._initialize_skus()

    def _initialize_skus(self):
        self.skus = [sk for sk in self.prod]
```

#### **Catalog Class Naming Convention:**
- **File Name:** `{vendor_id}_catalog.py` (e.g., `252_catalog.py`, `8022_catalog.py`)
- **Class Name:** `{Vendor_Short_Name}` from database (e.g., `Adams_and_Company`, `Desperate_Tin_Signs`)
- **Import Path:** Used by `update_waresitat.py` via dynamic `importlib` loading

#### **Testing Catalog Classes:**
```python
# Manual testing approach
csv_path = os.path.join('helper', 'csv', 'outfile', 'Vendor Name output.csv')
# Verify CSV exists and has expected columns
# Test product loading and field mapping
# Check for data validation issues
```

#### **Creating New Catalog Classes:**

1. **Determine Data Source:**
   - Check if vendor has Excel file in `xls/{vendor_id}.xls`
   - If not, use CSV from `helper/csv/outfile/{vendor_name} output.csv`

2. **Map CSV Fields to Schema:**
   - Standard CSV order: name,sku,cat,desc,stock,sale,set,custom,size,seller,min1,price1,min2,price2,min3,price3,multi,dir400,dir160,img400,img160,desc2,option,dir800,img800
   - Handle missing fields (e.g., `isUpdateAvailable` often missing from CSV)
   - Clean data: remove $ signs, validate numbers, extract filenames from URLs

3. **Data Validation Best Practices:**
   - Skip empty rows and products without SKUs
   - Handle price formatting ($ removal, rounding)
   - Validate numeric fields before conversion
   - Extract image filenames from full URLs
   - Provide fallback values for missing data

4. **Error Handling:**
   - Continue processing despite individual row errors
   - Log warnings for problematic data
   - Graceful handling of missing CSV files

### Data Synchronization System (`update_waresitat.py`)

**Purpose**: Synchronizes scraped vendor data with master "Waresitat" catalog files, providing Excel outputs for business operations.

**Core Workflow**:
1. **Load Data**: Import vendor catalog class and existing master data
2. **Compare Products**: Match by SKU across catalog and master datasets
3. **Update Changes**: Sync prices, stock, descriptions, images
4. **Add New Items**: Include newly discovered products
5. **Remove Inactive**: Clean up discontinued products
6. **Generate Excel**: Create business-ready XLS files

**Data Model**: Comprehensive product schema with 25+ fields:
```
CSV Format (25 columns): name,sku,cat,desc,stock,sale,set,custom,size,seller,min1,price1,min2,price2,min3,price3,multi,dir400,dir160,img400,img160,desc2,option,dir800,img800
Product Schema (26 fields): adds isUpdateAvailable field for tracking changes
```

### Waresitat Master Data System

**Location**: `src_py3/helper/waresitat_class.py`
**Purpose**: Container for consolidated product data across all vendors
**Features**:
- SKU-based product indexing
- Multi-format support (Northlight, Waresitat modes)
- Numeric validation and rounding
- Product addition and SKU management

### Database-Driven Configuration

**Vendor Gateway**: `src_py3/helper/gateway.py`
- MySQL database integration for vendor metadata
- Dynamic vendor class loading via `importlib`
- Image directory and filename configuration

## Data Flow Architecture

### Scraping Pipeline
1. **Input**: Missing SKUs from `helper/csv/outfile/noimg/{vendor}.csv`
2. **Search**: Vendor-specific search via `search_item()`
3. **Scrape**: Navigate product pages, extract data via `get_info()`
4. **Storage**: Save to `ActiveRecord` and backup CSV
5. **Output**: Final CSV at `helper/csv/outfile/{vendor} output.csv`

### Catalog Management Pipeline
1. **Scrape**: Individual vendor scrapers collect data
2. **Catalog**: Data organized into numbered catalog classes
3. **Synchronize**: `update_waresitat.py` compares with master data
4. **Update**: Changes applied to Waresitat master files
5. **Export**: Excel files generated in `xls/output/waresitat/`

## Running Systems

### Scraping Commands
```bash
cd src_py3
python scraper_seleniumv3.py vendor_name sitewide  # Full site scrape
python scraper_seleniumv3.py vendor_name           # Missing items only
```

### Catalog Management
```bash
python update_waresitat.py vendor_id1 vendor_id2  # Update specific vendors
```

### Resume Functionality
- **File-based persistence**: `resume/{vendor}_resume.pkl`
- **Automatic recovery**: Resumes from last processed item
- **Progress tracking**: Saves processing state periodically

## WebDriver Configuration

Uses `undetected-chromedriver` with anti-detection measures in `helper/webdriver_config.py`:
- Prompts for headless mode on startup
- Includes stealth options and user agent spoofing
- Maximizes window and clears cookies
- Automatic ChromeDriver management via `webdriver-manager`

## File Organization

- `src_py3/` - Main Python 3 codebase
- `vendor/` - Individual scraper classes (`*_class.py`) and catalog processors (`*_catalog.py`)
- `helper/` - Core framework (domainobject, gateway, waresitat, etc.)
- `xls/output/waresitat/` - Excel catalog outputs
- `xls/output/bhbt/` - Buy Here Buy There outputs
- `csv/outfile/` - CSV data files
- `resume/` - Resume state files
- Root directory - Legacy Python 2 scripts (deprecated)

## Scalability & Performance

### Current Architecture
- **69 vendor classes** with individual scrapers
- **512K+ lines of code** across the system
- **98MB+ CSV data files** for large catalogs
- **Sequential processing** with single-threaded execution

### Performance Characteristics
- **Single-threaded bottleneck**: 1.03s for 10 items (9.9x slower than optimal)
- **Memory-intensive**: Loads entire catalogs into memory
- **File I/O heavy**: Multiple read/write operations per vendor

### Enhancement Options

#### Immediate Improvements (Low Risk)
- **Async Processing**: Convert to concurrent batch processing (9.9x speedup potential)
- **Error Recovery**: Enhanced exception handling and retry logic
- **Progress Monitoring**: Real-time status tracking and metrics

#### Medium-term Enhancements
- **Database Migration**: Replace CSV files with PostgreSQL/MySQL
- **Containerization**: Docker deployment for scalability
- **Configuration Management**: Centralized config files

#### Long-term Architecture
- **Microservices**: Separate scraping, processing, and API services
- **Distributed Processing**: Multi-node scraping with queue management
- **API-first Design**: RESTful interfaces for data access

## Development Patterns

### Error Handling
- Extensive retry logic with backup mechanisms
- Failed items saved to `*_output_fail_safe.csv`
- Progress tracking with `tqdm` and resume functionality
- Manual CAPTCHA handling prompts

### Anti-Detection Measures
- Random delays between actions (configurable per vendor)
- Character-by-character password entry with random timing
- Smooth scrolling simulation
- User agent rotation and browser fingerprinting countermeasures

### Vendor-Specific Adaptations
Each vendor class handles unique challenges:
- **BigCommerce platforms**: Complex login flows with scrolling/CAPTCHA (`desperate_class.py`)
- **Custom e-commerce**: Varied product page structures and authentication
- **Option handling**: Products with multiple sizes, colors, variants

## Testing & Debugging

- Use `test.bat` for batch processing multiple vendors
- Check `debug.log` and `geckodriver.log` for browser issues
- Backup files serve as recovery points during development
- Progress bars show real-time scraping status
- Resume files enable interrupted process recovery

## Dependencies

Key packages in `requirements.txt`:
- `selenium==4.28.1` - Web automation
- `undetected-chromedriver==3.5.5` - Anti-detection
- `beautifulsoup4==4.12.2` - HTML parsing fallback
- `tqdm==4.66.1` - Progress bars
- `xlwt==1.3.0` - Excel file writing
- `xlrd==2.0.1` - Excel file reading
- `mysql-connector-python==8.0.33` - Database connectivity
- `webdriver-manager==4.0.1` - Automatic driver management

## Business Context

This system supports wholesale product catalog management for multiple vendors, providing:
- **Automated data synchronization** between vendor websites and master catalogs
- **Pricing tier management** with complex wholesale discount structures
- **Inventory tracking** across 69+ vendor relationships
- **Excel report generation** for business operations and purchasing decisions
- **Change detection** and update flagging for modified products

Run all commands from `src_py3/` directory to ensure proper module imports and path resolution.