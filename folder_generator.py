import os,xlrd,xlwt,csv

def main():
	with open("./csv/outfile/vendor_ids.csv") as infile:
		reader = csv.reader(infile)
		os.chdir("D:\Dropbox\Web Updates 2014\Waresitat Images")
		for line in reader:
			dr = line[1].replace("/","-")+"/800x800/"
			if not os.path.exists(dr):
				print dr
				os.makedirs(dr)

if __name__ == "__main__":
	main()