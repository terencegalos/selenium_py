import time,csv,os,sys,sqlite3,datetime

# to be added feature, vendor independent
# vendor = sys.arg[0]

# date checked
shipping_date = sys.argv[1]

# use this dictionary as a reference for K&K product info
f = {"sku":0,"name":1,"cat":2,"avail":4,"shipdate":6,"min1":7,"price1":8,"min2":9,"price2":10,"dim":15,"sale":16}

# table to insert
tables = ['tbl_kkjewelry','tbl_kksale','tbl_kkmain']



# logic for stock availability and shipping dates; uses element 4 and 3 respectively
# @param table; db table to insert info
# @param l; row to get info
# @param shipping_date; stock date check
# @param cur; sql tb pointer
def stock_check(table,l,shipping_date,cur):
    if int(l[4]) <= 0:
        if datetime.datetime.strptime(str(l[3][4:6]+"-"+l[3][6:8]+"-"+l[3][:4]),'%m-%d-%Y') < datetime.datetime.now(): # check if ETA is way past current date
			l = l[:4] + ("In stock & shipping checked (%s)" % shipping_date,) + l[5:]
        else:
			l = l[:4] + ("Out of stock - order to ship after %s" %l[3][4:6]+"-"+l[3][6:8]+"-"+l[3][:4],) + l[5:]
        
    else:
        l = l[:4] + ("In stock & shipping checked (%s)" % shipping_date,) + l[5:]
        
    print l
    cur.execute('insert into '+table+' values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',l)


# open db connection and create 3 new tables, drop first if already exists
con = None
try:
    con = sqlite3.connect("waresitat.db")
    cur = con.cursor()
    
    cur.executescript("""
    drop table if exists tbl_kkjewelry; 
    drop table if exists tbl_kkmain; 
    drop table if exists tbl_kksale;
    
    create table tbl_kkjewelry (name text,sku text,cat text,shipdate int,avail text,sale int,pack int,custom int,dim text,bestseller int,min1 int,price1 int,min2 int,price2 int,min3 int,price3 int,multi int,dir400 text,dir160 text,img400 text,img160 text,desc2 text,option text,dir800 text,img800 text);
    create table tbl_kksale (name text,sku text,cat text,shipdate int,avail text,sale int,pack int,custom int,dim text,bestseller int,min1 int,price1 int,min2 int,price2 int,min3 int,price3 int,multi int,dir400 text,dir160 text,img400 text,img160 text,desc2 text,option text,dir800 text,img800 text);
    create table tbl_kkmain (name text,sku text,cat text,shipdate int,avail text,sale int,pack int,custom int,dim text,bestseller int,min1 int,price1 int,min2 int,price2 int,min3 int,price3 int,multi int,dir400 text,dir160 text,img400 text,img160 text,desc2 text,option text,dir800 text,img800 text);
    """)

except sqlite3.Error,e:
	print "Error %s" % e.args[0]
	sys.exit(1)
    


# get K&K csv form into a csv reader object
csvfile = open("./csv/infile/kk_form.csv","rb")
readerObj = csv.reader(csvfile)



# loop csv reader object
for line in readerObj:

    if readerObj.line_num not in range(1,6):
        #this line get the values in required order
        l = (repr(line[f['name']]).encode("utf-8").rstrip(),line[f['sku']],line[f['cat']],line[f['shipdate']],line[f['avail']].rstrip(),line[f['sale']].rstrip(),"","",repr(line[f['dim']]).encode("utf-8").rstrip(),"",line[f['min1']],line[f['price1']],line[f['min2']],line[f['price2']],"","",line[f['min1']],"K&K400","K&K160","","","","","","")
        print l[4]
        print type(l[4])
        
        # logic if row belongs to main, sale or jewelry
        # this logic is specific to K&K
        if "JWL" in line[f['cat']]:
            print "JWL detected. Sleeping..."
            stock_check(tables[0],l,shipping_date,cur)
                
        elif line[f['sale']].strip() is not "":
            print "Sale detected. Sleeping..."
            stock_check(tables[1],l,shipping_date,cur)
                
        else:
            print "Main selected. Sleeping..."
            stock_check(tables[2],l,shipping_date,cur)

                
# retrieve K&K tables and save to csv file
for tb in tables:
    # get all items in table
    cur.execute('select * from %s' % tb)
    row = cur.fetchall()
    
    # save to csv file
    outfile = open('./csv/outfile/%s.csv' % tb,"wb")
    writer = csv.writer(outfile)
    writer.writerows(row)