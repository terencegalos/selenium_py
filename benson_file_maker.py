import csv
import time
import xlrd

class Item:
        def __init__(self,part,row):
                self.name = row[0].value
                self.sku = row[1].value
                self.cat = row[2].value
                self.desc = row[3].value
                self.min = row[11].value
                self.price = part
                self.multi = row[17].value
                self.dir400 = row[18].value
                self.dir160 = row[19].value
                self.img400 = row[21].value
                self.img160 = row[21].value
                self.dir800 = row[24].value
                self.img400 = row[25].value


def main():
        xls = xlrd.open_workbook("./xls/benson.xls")
        rsheet = xls.sheet_by_index(0)
        all = []

        out = []

        for x in range(rsheet.nrows):
                print "\n"+str(rsheet.row(x))+"\n"
                if "|" in rsheet.row(x)[27].value:
                        multi = rsheet.row(x)[27].value.split("|")
                        for part in multi:
                                item = Item(part,rsheet.row(x))
                                print dir(item)
                                all.append(item)
                
        


        


if __name__ == "__main__":
    main()