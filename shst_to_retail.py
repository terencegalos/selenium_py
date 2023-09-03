import xlrd,xlwt,os,sys,json
from gateway import Vendor

# vendor = sys.argv[1]
# dir = "C:\Dropbox\SHST Files\SHST Updated Sheet 2018\\"
dir = "C:/Dropbox/SHST Files/BRANDS Updated Sheet 2019/"

js = {
"Audreys_Your_Hearts_Delight_Products_SHST.xls":"/data/vendors/10953/products/",
"Adams_&_Company_Products_SHST.xls":"/data/vendors/10948/products/",
"Capitol_Earth_Rugs_Products_SHST.xls":"/data/vendors/10976/products/",
"Amish_Star_SHST.xls":"/data/vendors/10999/products/",
"Wholesale_Home_Decor_Products_SHST.xls":"/data/vendors/10968/products/",
"Raghu_Home_Collection_Products_SHST.xls":"/data/vendors/10972/products/",
"J&J_Wire_SHST.xls":"/data/vendors/11015/products/",
"Floral_Treasure_SHST.xls":"/data/vendors/11013/products/",
"Bethany_Lowe_SHST.xls":"/data/vendors/10967/products/",
"Pine_Valley_Pictures_SHST.xls":"/data/vendors/11054/products/",
"Vickie_Jeans_Creations_SHST.xls":"/data/vendors/10997/products/",
"Honey_&_Me_SHST.xls":"/data/vendors/10966/products/",
"Artistic_Reflections_SHST.xls":"/data/vendors/10990/products/",
"Designs_Combined_SHST.xls":"/data/vendors/10980/products/",
"Hip_Signs_for_Cool_Folks_SHST.xls":"/data/vendors/11114/products/",
"Sallyeander_Soaps_SHST.xls":"/data/vendors/11008/products/",
"a_cheerful_giver_shst.xls":"/data/vendors/10954/products/",
"A_Homestead_Shoppe_SHST.xls":"/data/vendors/11110/products/",
"Desma_Group_Home__Gift_SHST.xls":"/data/vendors/11110/products/",
u"Homespice_D\xe9cor_SHST.xls":"/data/vendors/11115/products/",
"KMI_SHST.xls":"/data/vendors/10993/products/",
"Wing_Tai_Trading_SHST.xls":"/data/vendors/11118/products/",
"JanMichael's_Art_&_Home_Products_SHST.xls":"/data/vendors/10962/products/",
"Ann_Clark_Cookie_Cutters_SHST.xls":"/data/vendors/11014/products/",
"Warm_Glow_Candles_SHST.xls":"/data/vendors/10991/products/",
"The_Country_House_Collection_SHST.xls":"/data/vendors/10955/products/",
"Blossom_Bucket_SHST.xls":"/data/vendors/10952/products/",
"Country_Home_Creations_SHST.xls":"/data/vendors/11111/products/",
"Chesapeake_Bay_&_JD_Yeatts_SHST.xls":"/data/vendors/11001/products/",
"Pine_Valley_Pictures_SHST.xls":"/data/vendors/11054/products/",
"Miller_Decor_SHST.xls":"/data/vendors/10985/products/",
"Impressions_on_Market_SHST.xls":"/data/vendors/10998/products/",
"DNS_Designs_SHST.xls":"/data/vendors/11011/products/",
"Whiskey_Mountain_SHST.xls":"/data/vendors/10996/products/",
"Ragon_House_Collection_SHST.xls":"/data/vendors/10950/products/",
"Capabunga_SHST.xls":"/data/vendors/11007/products/",
"Beyond_Borders_SHST.xls":"/data/vendors/10995/products/",
"Pine_Creek_Four_Corners_Products_SHST.xls":"/data/vendors/10979/products/",
"Honey_House_Naturals_SHST.xls":"/data/vendors/11012/products/",
"Rose_of_Sharon_Home_Fragrances_SHST.xls":"/data/vendors/10992/products/"	,
"Carson_Home_Accents_SHST.xls":"/data/vendors/11004/products/",
"Craft_Outlet_-_Olde_Memories_SHST.xls":"/data/vendors/10984/products/",
"Black_Crow_Candles_SHST.xls":"/data/vendors/10973/products/",
"Cowgirl_Chocolates_SHST.xls":"/data/vendors/11112/products/",
"Special_T_Imports_SHST.xls":"/data/vendors/10983/products/",
"Bittersweetspring_SHST.xls":"/data/vendors/10994/products/",
"Primitives_at_Crow_Hollow_SHST.xls":"/data/vendors/11116/products/",
"Barn_Candles_SHST.xls":"/data/vendors/11000/products/",
"Simply_Vintage_Soy_SHST.xls":"/data/vendors/11006/products/",
"American_Dakota_Rugs_SHST.xls":"/data/vendors/11003/products/",
"Kraft_Klub_SHST.xls":"/data/vendors/10963/products/",
"Desperate_Tin_Signs_SHST.xls":"/data/vendors/11005/products/",
"Delton_Products_SHST.xls":"/data/vendors/10988/products/",
"Bright_Ideas_SHST.xls":"/data/vendors/10977/products/",
"McCall's_Candles_SHST.xls":"/data/vendors/11002/products/",
"The_Crafters_Loft_SHST.xls":"/data/vendors/11044/products/",
"VIP_Home_and_Garden_Products_SHST.xls":"/data/vendors/10981/products/",
"Hanna's_Handiworks_SHST.xls":"/data/vendors/10969/products/",
"Market_Street_Wholesale_SHST.xls":"/data/vendors/11009/products/",
"Timeless_By_Design_SHST.xls":"/data/vendors/11117/products/",
"GAR_Wholesale_Inc._SHST.xls":"/data/vendors/11113/products/",
"Irvin's_Tinware_SHST.xls":"/data/vendors/10978/products/",
"Flag_Galore_Decor_SHST.xls":"/data/vendors/10989/products/",
"Barn_Cat_Mercantile_SHST.xls":"/data/vendors/11046/products/",
"Lifeforce_SHST.xls":"/data/vendors/11121/products/",
"Crossroads_Candles_SHST.xls":"/data/vendors/11076/products/",
"Papas_Candle_Shoppe_SHST.xls":"/data/vendors/11094/products/",
"Things_Western_SHST.xls":"/data/vendors/11095/products/",
"Christian_Art_Gifts_SHST.xls":"/data/vendors/11092/products/",
"Lambright_Country_Chimes_SHST.xls":"/data/vendors/11108/products/",
"California_Home_and_Garden_SHST.xls":"/data/vendors/11120/products/",
"Maine_Wooden_Bouys_SHST.xls":"/data/vendors/11122/products/",
"The_Hearthside_Collection_SHST.xls":"/data/vendors/11097/products/",
"The_Crafters_Loft_SHST.xls":"/data/vendors/11044/products/"}

class Retail:
	
	store = []

	def makeLine(self,row,f):
		line = []
		line.append(row[0].value)
		line.append(row[1].value)
		line.append(row[2].value)
		line.append(row[3].value)
		line.append(row[5].value)
		line.append(row[15].value if "MSRP" not in str(row[15].value) else "Unit Price")
		image = js[f.decode("latin-1")]+str(row[13].value) if "product images" not in str(row[13].value).lower() else "Product Images"
		line.append(image)
		line.append(25 if row[14].value != "Quantity" else row[14].value)
		line.append("") #remove sale as it causes issues
		line.append(row[17].value)
		line.append(row[18].value)
		line.append(row[19].value)
		line.append(row[20].value)
		line.append(row[21].value)
		line.append(row[22].value)
		line.append(row[23].value)
		line.append(row[4].value)
		return line

	
	def ensure_unicode(self,v):
		if isinstance(v,str):
			v = v.decode("utf-8")
		return unicode(v)
	
	def addProduct(self,row,f):
		#print row
		line = self.makeLine(row,f)
		self.store.append(line)
	
def writeXLS(r_obj,fname):
	book = newXLS()
	sheet = book.add_sheet("Sheet1")
	for n,line in enumerate(r_obj.store):
		row = sheet.row(n)
		for c,val in enumerate(line):
			row.write(c,val)
	fname,ext = os.path.splitext(fname)
	book.save("C:\Dropbox\SHST Files\RETAIL SHEET SHST\\"+fname+"_retail"+ext)
	
def newXLS():
	wbook = xlwt.Workbook()
	return wbook

def main():
	# files = [file for file in os.listdir(dir) if "_" in file] # get all files in directory
	# print files
	files = sys.argv[1]
	for file in [files]:
		# print file
		if '_' not in file.lower():
			continue
		if 'mullberry' in file.lower():
			continue
		# if "homespice" in file.lower() or 'hearthside' in file.lower():
			# continue
		print file
		myretail = Retail()
		rbook = xlrd.open_workbook(dir+"\\"+file)
		rsheet = rbook.sheet_by_index(0)
		for n in range(rsheet.nrows):
			row = rsheet.row(n)
			myretail.addProduct(row,file)
			
		writeXLS(myretail,file)
		myretail.store[:] = []
			
	
	
if __name__ == "__main__":
	main()