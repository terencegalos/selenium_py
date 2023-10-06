
class gateway:

    
    def __init__(self,obj=None):

        atts = [att for att in self.getFieldNames()]
        
        if obj is None: # fill values first: just empty string
            for x in range(len(atts)):
                setattr(self,atts[x],"")

        else: # new instance with obj param
            for x in range(len(atts)):
                setattr(self,atts[x],obj[x])

        # print "Gateway initialized."

    
    def getFieldNames(self):
        return ["name","sku","cat","desc","stock","sale","set","custom","size","seller","min1","price1","min2","price2","min3","price3","multi","dir400","dir160","img400","img160","desc2","option","dir800","img800","isUpdateAvailable"]


        
    def retrieve(self):
        atts = [att for att in self.getFieldNames()]
        props = [getattr(self,att) for att in atts]
        return props

		
    def __str__(self):
        atts = [att for att in self.getFieldNames()]
        props = [getattr(self,att) for att in atts]
        return ", ".join([str(att) for att in props])
        
        
#setters
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name = value
    @property
    def sku(self):
        return self._sku
    @sku.setter
    def sku(self,value):
        self._sku = value
    @property
    def cat(self):
        return self._cat
    @cat.setter
    def cat(self,value=""):
        self._cat = value
    @property
    def desc(self):
        return self._desc
    @desc.setter
    def desc(self,value):
        self._desc = value
    @property
    def stock(self):
        return self._stock
    @stock.setter
    def stock(self,value=""):
        self._stock = value
    @property
    def set(self):
        return self._set
    @set.setter
    def set(self,value=""):
        self._set = value
    @property
    def custom(self):
        return self._custom
    @custom.setter
    def custom(self,value=""):
        self._custom = value
    @property
    def size(self):
        return self._size
    @size.setter
    def size(self,value=""):
        self._size = value
    @property
    def seller(self):
        return self._seller
    @seller.setter
    def seller(self,value=""):
        self._seller = value
    @property
    def min1(self):
        return self._min1
    @min1.setter
    def min1(self,value):
        self._min1 = value
    @property
    def price1(self):
        return self._price1
    @price1.setter
    def price1(self,value):
        self._price1 = value
    @property
    def min2(self):
        return self._min2
    @min2.setter
    def min2(self,value):
        self._min2 = value
    @property
    def price2(self):
        return self._price2
    @price2.setter
    def price2(self,value):
        self._price2 = value
    @property
    def min3(self):
        return self._min3
    @min3.setter
    def min3(self,value):
        self._min3 = value
    @property
    def price3(self):
        return self._price3
    @price3.setter
    def price3(self,value):
        self._price3 = value
    @property
    def multi(self):
        return self._multi
    @multi.setter
    def multi(self,value):
        self._multi = value
    @property
    def dir400(self):
        return self._dir400
    @dir400.setter
    def dir400(self,value="Raghu400"):
        self._dir400 = value
    @property
    def dir160(self):
        return self._dir160
    @dir160.setter
    def dir160(self,value="Raghu160"):
        self._dir160 = value
    @property
    def img400(self):
        return self._img400
    @img400.setter
    def img400(self,value):
        self._img400 = value
    @property
    def img160(self):
        return self._img160
    @img160.setter
    def img160(self,value):
        self._img160 = value
    @property
    def desc2(self):
        return self._desc2
    @desc2.setter
    def desc2(self,value):
        self._desc2 = value
    @property
    def option(self):
        return self._option
    @option.setter
    def option(self,value=""):
        self._option = value
    @property
    def dir800(self):
        return self._dir800
    @dir800.setter
    def dir800(self,value="Raghu800"):
        self._dir800 = value
    @property
    def img800(self):
        return self._img800
    @img800.setter
    def img800(self,value):
        self._img800 = value
    @property
    def isUpdateAvailable(self):
        return self._isUpdateAvailable
    @isUpdateAvailable.setter
    def isUpdateAvailable(self,value):
        self._isUpdateAvailable = value