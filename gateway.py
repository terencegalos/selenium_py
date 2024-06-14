import csv, os
# Make vendor info object with name,imgdir,filename etc.
class Vendor():
	name = None
	is_available = False
	# IMPORTANT! use CODE to initialize vendor
	def __init__(self,id):
		with open(os.path.dirname(__file__)+"/csv/outfile/vendor_ids.csv","rb") as infile:
			rows = csv.reader(infile)
			for line in rows:
				if id == line[0]:
					self.is_available = True
					self.name = line[1]
					self.classname = line[2]
					self.filename = line[3]
					self.code = line[0]
					self.img160 = line[4]
					self.img400 = line[5]
					self.img800 = line[6]
					self.shst = line[7]
					self.bhbt = line[8]
			if self.is_available == False:
				print "Vendor id not found."
			
					
		self._paramcheck()
		
	def _paramcheck(self):
		if self.name and self.filename and self.code and self.img160 and self.img400 and self.img800:
			return True