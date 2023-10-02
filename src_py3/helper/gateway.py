import mysql.connector, helper.config as config#, csv, os
# Make vendor info object with name,imgdir,filename etc.
class Vendor():
	name = None
	# IMPORTANT! use CODE to initialize vendor
	def __init__(self,id):
		conn = mysql.connector.connect(
			host=config.DBHOST,
			user=config.DBUSER,
			password=config.DBPASS,
			database=config.DBNAME
		)
		sql = "select * from vendors where id=%s"
		cur = conn.cursor()
		
		params = (id,)
		cur.execute(sql,params)

		# with open(os.path.dirname(__file__)+"/csv/outfile/vendor_ids.csv","rb") as infile:
		# rows = csv.reader(infile)
		rows = cur.fetchall()
		for line in rows:
			id, name,short_name,file_name,image_160px,image_400px,image_800px,shst_file_name,bhbt_file_name = line
			self.name = name
			self.classname = short_name
			self.filename = file_name
			self.code = id
			self.img160 = image_160px
			self.img400 = image_400px
			self.img800 = image_800px
			self.shst = shst_file_name
			self.bhbt = bhbt_file_name

		conn.close()
					
		self._paramcheck()
		
	def _paramcheck(self):
		if self.name and self.filename and self.code and self.img160 and self.img400 and self.img800:
			return True
		
	def __str__(self):
		return f"Name: {self.name}, ClassName: {self.classname}, FileName: {self.filename}, Code: {self.code}, Img160: {self.img160}, Img400: {self.img400}, Img800: {self.img800}, SHST: {self.shst}, BHBT: {self.bhbt}"
