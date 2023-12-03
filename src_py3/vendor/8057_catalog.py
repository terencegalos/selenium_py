from helper.xls_getter import TableData
import datetime, time

class Hannas_Handiworks():
    prod = {}
    skus = None
	
    def is_num(self,x):
        try:
            float(x)
            return True
        except:
            return False

    def __init__(self,vendor,mode=2):
        table = TableData(vendor,mode) # instantiate vendor file into an object
        rsheet = table.getSheet()
        for x in range(1,rsheet.nrows):
            try:
                float(rsheet.row(x)[0].value)
                sku = str(int(rsheet.row(x)[0].value))
            except:
                sku = " ".join(rsheet.row(x)[0].value.split())
            self.prod[sku] = {}
            self.prod[sku]['name'] = rsheet.row(x)[1].value
            self.prod[sku]['sku'] = sku
            self.prod[sku]['cat'] = ''
            self.prod[sku]['desc'] = ''
            self.prod[sku]['stock'] = ''
            self.prod[sku]['sale'] = float(rsheet.row(x)[4].value.split("/")[1].strip("$")) if rsheet.row(x)[4].value != '' and self.is_num(rsheet.row(x)[4].value.split("/")[1].strip("$")) and rsheet.row(x)[4].value.split("/")[0] == rsheet.row(x)[3].value.split("/")[0] else ''
            self.prod[sku]['set'] = ""
            self.prod[sku]['custom'] = ""
            self.prod[sku]['size'] = ''
            self.prod[sku]['top'] = ""
            self.prod[sku]['min'] = float(rsheet.row(x)[3].value.split("/")[0]) if self.is_num(rsheet.row(x)[3].value.split("/")[0]) else rsheet.row(x)[3].value
            self.prod[sku]['price1'] = float(rsheet.row(x)[3].value.split("/")[1].strip("$")) if self.is_num((rsheet.row(x)[3].value.split("/")[1].strip("$"))) else rsheet.row(x)[3].value
            self.prod[sku]['min2'] = float(rsheet.row(x)[4].value.split("/")[0]) if rsheet.row(x)[4].value != '' and self.is_num(rsheet.row(x)[4].value.split("/")[0]) and rsheet.row(x)[4].value.split("/")[0] !=  rsheet.row(x)[3].value.split("/")[0] else ''
            self.prod[sku]['price2'] = float(rsheet.row(x)[4].value.split("/")[1].strip("$")) if rsheet.row(x)[4].value != '' and self.is_num(rsheet.row(x)[4].value.split("/")[1].strip("$")) and rsheet.row(x)[4].value.split("/")[0] !=  rsheet.row(x)[3].value.split("/")[0] else ''
            self.prod[sku]['min3'] = float(rsheet.row(x)[5].value.split("/")[0]) if rsheet.row(x)[5].value!= '' and self.is_num(rsheet.row(x)[5].value.split("/")[0]) else rsheet.row(x)[5].value
            self.prod[sku]['price3'] = float(rsheet.row(x)[5].value.split("/")[1].strip("$")) if rsheet.row(x)[5].value != '' and self.is_num(rsheet.row(x)[5].value.split("/")[1].strip("$")) else rsheet.row(x)[5].value
            self.prod[sku]['multi'] = float(rsheet.row(x)[3].value.split("/")[0]) if self.is_num(rsheet.row(x)[3].value.split("/")[1].strip("$")) else rsheet.row(x)[3].value
            self.prod[sku]['img400'] = "Hannas400"
            self.prod[sku]['img160'] = "Hannas160"
            self.prod[sku]['jpg400'] =""
            self.prod[sku]['jpg160'] = ""
            self.prod[sku]['desc2'] = ""
            self.prod[sku]['opt'] = ""
            self.prod[sku]['img800'] = "Hannas800"
            self.prod[sku]['jpg800'] = ""
            self.prod[sku]['isUpdateAvailable'] = ""
			
        self._initialize_skus()
		
    def _initialize_skus(self):
        self.skus = [sk for sk in self.prod]
		
    def __str__(self):
        return "\n".join(self.skus)