import csv,xlwt,xlrd

keepers = {'Papa':{'opt':'Lid:|Black|Copper','code':'jp','size':'34oz up to 155hrs','price':'12','min':'2'},'Mama':{'opt':'Lid:|Black|Copper','code':'jm','size':'22oz/up to 25 hours','price':'10','min':'2'},'Baby':{'opt':'Lid:|Black|Copper','code':'jnb','size':'6oz/up to 30 hours','min':'2','price':'4.50'},'Votives':{'code':'v','size':'18/cs','min':'18','price':'0.94'},'Melts':{'code':'fk','size':'8/cs','min':'8','price':'1.75'}}
cheerful = {'CC':{'code':'cc','size':'24oz/up to 135hrs.','price':'10','min':'2'},'CS':{'code':'cs','size':'16oz/up to 80 hrs.','min':'2','price':'7.50'},'CB':{'code':'cb','size':'6oz/up to 30hrs','min':'2','price':'4.5'},'CV':{'code':'cv','size':'18/cs','min':'18','price':'0.94'},'M':{'code':'m','size':'8/cs','min':'8','price':'1.75'}}
# [text:u' Sage & Citrus', text:u'Lid:|Black|Copper', text:u'Light Green', number:55.0]

def main():
	rbook = xlrd.open_workbook("./xls/acg.xls")
	rsheet = rbook.sheet_by_index(0)
	
	all = []
	
	for line in range(rsheet.nrows):
		row = rsheet.row(line)
		
		for data in cheerful.iteritems():
			# print data[1]['code']
			item = []
			name = data[0]+" -"+row[0].value.encode("utf-8")+" - "+row[2].value.encode("utf-8")
			sku = data[1]['code']+str(row[3].value)
			size = data[1]['size']
			min = data[1]['min']
			price = data[1]['price']
			try:
				opt = data[1]['opt']
			except:
				opt = ""
			item.append([name,sku,size,min,price,opt])
			all.extend(item)
			
			
	# for l in all:
		# print l
	with open("./csv/outfile/acg.csv","wb") as outfile:
		writer = csv.writer(outfile)
		writer.writerows(all)
			






if __name__ == "__main__":
	main()