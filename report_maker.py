import csv,os

class Report():
	store = []
	def add(self,i):
		self.store.append(i)
		
		

class Item():
	def __init__(self,line):
		self.po = line[0]
		self.name = line[1]
		self.street = line[2]
		self.city = line[3]
		self.state = line[4]
		self.country = line[5]
		self.zip = line[6]
		self.phone = line[7]
		self.first = line[8]
		self.last = line[9]
		self.email = line[10]
		self.vendor = line[12]
		self.orderdate = line[13]
		self.subtotal = line[14]
		
	def retrieve(self):
		return [self.po,\
		self.name,\
		self.street,\
		self.city,\
		self.state,\
		self.country,\
		self.zip,\
		self.phone,\
		self.first,\
		self.last,\
		self.email,\
		self.vendor,\
		self.orderdate,\
		self.subtotal]

def main():
	with open("./csv/infile/export.csv","rb") as infile:
		rows = csv.reader(infile)
		rp = Report()
		
		for line in rows:
			rp.add(Item(line))
			
		vendors = [r.vendor for r in rp.store]
		
		for vendor in vendors:
			items = []
			items.append(["InvoiceNumber","CompanyName","StreetAddress","City","StateProvince","Country","ZipPostalCode","Phone","FirstName","LastName","CustomerEmail","Vendor_Name","DateOrdered","Subtotal"])
			for r in rp.store:
				if vendor in r.vendor:
					items.append(r.retrieve())
			with open("C:/Dropbox/Sherie Docs/Reports/"+vendor+".csv","wb") as outfile:
				writer = csv.writer(outfile)
				writer.writerows(items)
				
			
	
if __name__ == "__main__":
	main()