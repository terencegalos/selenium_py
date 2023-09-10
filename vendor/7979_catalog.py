from xls_getter import TableData
import datetime

class Jones_Rustic_Signs():
    prod = {}
    skus = None
    disc = False
    
    def is_num(self,num):
        try:
            float(num)
            return True
        except:
            return False

    def __init__(self,vendor,mode=2):
        
        table = TableData(vendor,mode) # instantiate vendor file into an object
        rsheet = table.getSheet()
        
        for x in range(1,rsheet.nrows):
            if not self.is_num(rsheet.row(x)[8].value):
                continue

            try:
                float(rsheet.row(x)[2].value)
                sku = str(rsheet.row(x)[2].value)
            except:
                sku = "".join(rsheet.row(x)[2].value.split())

            self.prod[sku] = {}
            self.prod[sku]['name'] = rsheet.row(x)[4].value
            self.prod[sku]['sku'] = sku
            self.prod[sku]['cat'] = ""
            self.prod[sku]['desc'] = ""
            self.prod[sku]['stock'] = ""
            self.prod[sku]['sale'] = ""
            self.prod[sku]['set'] = ""
            self.prod[sku]['custom'] = ""
            self.prod[sku]['size'] = ""
            self.prod[sku]['top'] = ""
            self.prod[sku]['min'] = 1
            self.prod[sku]['price1'] = round(float(rsheet.row(x)[8].value),2)
            self.prod[sku]['min2'] = ""
            self.prod[sku]['price2'] = ""
            self.prod[sku]['min3'] = ""
            self.prod[sku]['price3'] = ""
            self.prod[sku]['multi'] = 1
            self.prod[sku]['img400'] = "jonesigns400"
            self.prod[sku]['img160'] = "jonesigns160"
            self.prod[sku]['jpg400'] = ""
            self.prod[sku]['jpg160'] = ""
            self.prod[sku]['desc2'] = ""
            self.prod[sku]['opt'] = ""
            self.prod[sku]['img800'] = "jonesigns160"
            self.prod[sku]['jpg800'] = ""
            self.prod[sku]['isUpdateAvailable'] = ""
        
        self._initialize_skus()
    
    def _initialize_skus(self):
        self.skus = [sk for sk in self.prod]
    
    def __str__(self):
        return "\n".join(self.skus)