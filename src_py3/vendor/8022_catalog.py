import csv
import os
from helper.table_gateway import gateway

class Desperate_Tin_Signs():
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

        # Path to the CSV output file from scraping
        csv_path = os.path.join(os.path.dirname(__file__), "..", "helper", "csv", "outfile", "Desperate Tin Signs output.csv")

        if not os.path.exists(csv_path):
            print(f"Warning: CSV file not found at {csv_path}")
            self._initialize_skus()
            return

        print(f"Loading data from CSV file: {csv_path}")

        try:
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                # Read CSV with proper handling of quoted fields
                reader = csv.reader(csvfile)

                for row_num, row in enumerate(reader, 1):
                    try:
                        # Skip empty rows
                        if not row or len(row) < 2:
                            continue

                        # Map CSV columns to gateway fields
                        # CSV format: name,sku,cat,desc,stock,sale,set,custom,size,seller,min1,price1,min2,price2,min3,price3,multi,dir400,dir160,img400,img160,desc2,option,dir800,img800
                        # Note: isUpdateAvailable is not in CSV, so we set it to empty
                        if len(row) >= 25:
                            name = row[0].strip()
                            sku = row[1].strip()
                            cat = row[2].strip()
                            desc = row[3].strip()
                            stock = row[4].strip()
                            sale = row[5].strip()
                            set_val = row[6].strip()
                            custom = row[7].strip()
                            size = row[8].strip()
                            seller = row[9].strip()
                            min1 = row[10].strip()
                            price1 = row[11].strip()
                            min2 = row[12].strip()
                            price2 = row[13].strip()
                            min3 = row[14].strip()
                            price3 = row[15].strip()
                            multi = row[16].strip()
                            dir400 = row[17].strip()
                            dir160 = row[18].strip()
                            img400 = row[19].strip()
                            img160 = row[20].strip()
                            desc2 = row[21].strip()
                            option = row[22].strip()
                            dir800 = row[23].strip()
                            img800 = row[24].strip()
                            isUpdateAvailable = ""  # Not in CSV
                        else:
                            # Handle shorter rows (fallback mapping)
                            name = row[0] if len(row) > 0 else ""
                            sku = row[1] if len(row) > 1 else ""
                            cat = row[2] if len(row) > 2 else ""
                            desc = row[3] if len(row) > 3 else ""
                            stock = ""
                            sale = ""
                            set_val = ""
                            custom = ""
                            size = ""
                            seller = ""
                            min1 = "1"
                            price1 = ""
                            min2 = ""
                            price2 = ""
                            min3 = ""
                            price3 = ""
                            multi = "1"
                            dir400 = "desperate400"
                            dir160 = "desperate160"
                            img400 = ""
                            img160 = ""
                            desc2 = ""
                            option = ""
                            dir800 = "desperate800"
                            img800 = ""
                            isUpdateAvailable = ""

                        # Skip items without SKU
                        if not sku:
                            continue

                        # Clean and validate price
                        if price1 and price1.startswith('$'):
                            price1 = price1[1:]  # Remove $ sign

                        # Convert numeric fields
                        try:
                            if price1 and self.is_num(price1):
                                price1 = round(float(price1), 2)
                            if min1 and self.is_num(min1):
                                min1 = float(min1)
                            if multi and self.is_num(multi):
                                multi = float(multi)
                        except:
                            pass

                        # Create product entry
                        self.prod[sku] = {
                            'name': name,
                            'sku': sku,
                            'cat': cat,
                            'desc': desc,
                            'stock': stock,
                            'sale': sale,
                            'set': set_val,
                            'custom': custom,
                            'size': size,
                            'top': '',
                            'min': min1,
                            'price1': price1,
                            'min2': min2,
                            'price2': price2,
                            'min3': min3,
                            'price3': price3,
                            'multi': multi,
                            'img400': img400,
                            'img160': img160,
                            'jpg400': img400.split('/')[-1] if img400 and '/' in img400 else img400,
                            'jpg160': img160.split('/')[-1] if img160 and '/' in img160 else img160,
                            'desc2': desc2,
                            'opt': option,
                            'img800': img800,
                            'jpg800': img800.split('/')[-1] if img800 and '/' in img800 else img800,
                            'isUpdateAvailable': isUpdateAvailable
                        }

                    except Exception as e:
                        print(f"Warning: Error processing row {row_num}: {e}")
                        continue

            print(f"Loaded {len(self.prod)} products from CSV")

        except Exception as e:
            print(f"Error reading CSV file: {e}")

        self._initialize_skus()

    def _initialize_skus(self):
        self.skus = [sk for sk in self.prod]

    def __str__(self):
        return "\n".join(self.skus)