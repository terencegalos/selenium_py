from helper.xls_getter import TableData
import time
import datetime

class Vickie_Jeans_Creations():
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
        
        stock = "placeholder"
        for x in range(rsheet.nrows):
            try:
                float(rsheet.row(x)[1].value)
                sku = str(int(rsheet.row(x)[1].value))
            except:
                sku = "".join(rsheet.row(x)[1].value.split())
                
            self.prod[sku] = {}
            self.prod[sku]['name'] = rsheet.row(x)[0].value
            self.prod[sku]['sku'] = rsheet.row(x)[1].value
            self.prod[sku]['cat'] = rsheet.row(x)[2].value
            self.prod[sku]['desc'] = rsheet.row(x)[3].value
            self.prod[sku]['stock'] = ""
            self.prod[sku]['sale'] = ""
            self.prod[sku]['set'] = rsheet.row(x)[6].value
            self.prod[sku]['custom'] = ""
            self.prod[sku]['size'] = rsheet.row(x)[8].value
            self.prod[sku]['top'] = ""
            self.prod[sku]['min'] = rsheet.row(x)[10].value
            self.prod[sku]['price1'] = rsheet.row(x)[11].value
            self.prod[sku]['min2'] = rsheet.row(x)[12].value
            self.prod[sku]['price2'] = rsheet.row(x)[13].value
            self.prod[sku]['min3'] = rsheet.row(x)[14].value
            self.prod[sku]['price3'] = rsheet.row(x)[15].value
            self.prod[sku]['multi'] = rsheet.row(x)[16].value
            self.prod[sku]['img400'] = "VickieJeans400"
            self.prod[sku]['img160'] = "VickieJeans160"
            self.prod[sku]['jpg400'] = rsheet.row(x)[19].value
            self.prod[sku]['jpg160'] = rsheet.row(x)[20].value
            self.prod[sku]['desc2'] = ""
            self.prod[sku]['opt'] = ""
            self.prod[sku]['img800'] = "VickieJeans800"
            self.prod[sku]['jpg800'] = rsheet.row(x)[24].value
            self.prod[sku]['isUpdateAvailable'] = ""

        self._initialize_skus()
    
    def _initialize_skus(self):
        self.skus = [sk for sk in self.prod]
    
    def __str__(self):
        return "\n".join(self.skus)
    
    def __len__(self):
        return len(self.prod)