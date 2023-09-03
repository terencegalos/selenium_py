import xlrd,xlwt,os,csv

def main():
	files = os.listdir("./xls/SHST Updated Sheet 2018/")
	for file in files:
		print file
		# if " " in file:
			# os.rename("./xls/SHST Updated Sheet 2018/"+file,"./xls/SHST Updated Sheet 2018/"+"_".join(file.split()))
	# vendors = []
	# with open("./csv/outfile/vendor_ids.csv","rb") as infile:
		# fread = csv.reader(infile)
		# for line in fread:
			# vendors.append(line[1])
			
	
	# files = os.listdir("./xls/SHST Updated Sheet 2018/")
	# for file in files:
		# for vendor in vendors:
			# if vendor in file:
				# os.rename("./xls/SHST Updated Sheet 2018/"+file,"./xls/SHST Updated Sheet 2018/"+"_".join(vendor.split())+"_SHST.xls")
	
	
if __name__ == "__main__":
	main()