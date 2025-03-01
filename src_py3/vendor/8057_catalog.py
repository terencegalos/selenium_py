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
            self.prod[sku]['name'] = rsheet.row(x)[4].value
            self.prod[sku]['sku'] = sku
            self.prod[sku]['cat'] = ''
            self.prod[sku]['desc'] = ''
            self.prod[sku]['stock'] = ''
            self.prod[sku]['sale'] = float(rsheet.row(x)[14].value) if rsheet.row(x)[11].value != '' and self.is_num(rsheet.row(x)[11].value) and rsheet.row(x)[11].value == rsheet.row(x)[13].value else ''
            self.prod[sku]['set'] = ""
            self.prod[sku]['custom'] = ""
            self.prod[sku]['size'] = rsheet.row(x)[6].value
            self.prod[sku]['top'] = ""
            self.prod[sku]['min'] = rsheet.row(x)[11].value#float(rsheet.row(x)[3].value.split("/")[0]) if self.is_num(rsheet.row(x)[3].value.split("/")[0]) else rsheet.row(x)[3].value
            self.prod[sku]['price1'] = round(float(rsheet.row(x)[12].value),2)#float(rsheet.row(x)[3].value.split("/")[1].strip("$")) if self.is_num((rsheet.row(x)[3].value.split("/")[1].strip("$"))) else rsheet.row(x)[3].value
            self.prod[sku]['min2'] = rsheet.row(x)[13].value if rsheet.row(x)[13].value != '' and self.is_num(rsheet.row(x)[13].value) and rsheet.row(x)[13].value !=  rsheet.row(x)[11].value else ''
            self.prod[sku]['price2'] = rsheet.row(x)[14].value if rsheet.row(x)[11].value != '' and self.is_num(rsheet.row(x)[11].value) and rsheet.row(x)[11].value !=  rsheet.row(x)[13].value else ''
            self.prod[sku]['min3'] = rsheet.row(x)[15].value#float(rsheet.row(x)[5].value.split("/")[0]) if rsheet.row(x)[5].value!= '' and self.is_num(rsheet.row(x)[5].value.split("/")[0]) else rsheet.row(x)[5].value
            self.prod[sku]['price3'] = rsheet.row(x)[16].value#float(rsheet.row(x)[5].value.split("/")[1].strip("$")) if rsheet.row(x)[5].value != '' and self.is_num(rsheet.row(x)[5].value.split("/")[1].strip("$")) else rsheet.row(x)[5].value
            self.prod[sku]['multi'] = rsheet.row(x)[11].value#float(rsheet.row(x)[3].value.split("/")[0]) if self.is_num(rsheet.row(x)[3].value.split("/")[1].strip("$")) else rsheet.row(x)[3].value
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