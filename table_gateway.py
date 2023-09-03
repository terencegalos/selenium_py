
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
        return self.name
    @name.setter
    def name(self,value):
        self.name = value
    @property
    def sku(self):
        return self.sku
    @sku.setter
    def sku(self,value):
        self.sku = value
    @property
    def cat(self):
        return self.cat
    @cat.setter
    def cat(self,value=""):
        self.cat = value
    @property
    def desc(self):
        return self.desc
    @desc.setter
    def desc(self,value):
        self.desc = value
    @property
    def stock(self):
        return self.stock
    @stock.setter
    def stock(self,value=""):
        self.stock = value
    @property
    def set(self):
        return self.set
    @set.setter
    def set(self,value=""):
        self.set = value
    @property
    def custom(self):
        return self.custom
    @custom.setter
    def custom(self,value=""):
        self.custom = value
    @property
    def size(self):
        return self.size
    @size.setter
    def size(self,value=""):
        self.size = value
    @property
    def seller(self):
        return self.seller
    @seller.setter
    def seller(self,value=""):
        self.seller = value
    @property
    def min1(self):
        return self.min1
    @min1.setter
    def min1(self,value):
        self.min1 = value
    @property
    def price1(self):
        return self.price1
    @price1.setter
    def price1(self,value):
        self.price1 = value
    @property
    def min2(self):
        return self.min2
    @min2.setter
    def min2(self,value):
        self.min2 = value
    @property
    def price2(self):
        return self.price2
    @price2.setter
    def price2(self,value):
        self.price2 = value
    @property
    def min3(self):
        return self.min3
    @min3.setter
    def min3(self,value):
        self.min3 = value
    @property
    def price3(self):
        return self.price3
    @price3.setter
    def price3(self,value):
        self.price3 = value
    @property
    def multi(self):
        return self.multi
    @multi.setter
    def multi(self,value):
        self.multi = value
    @property
    def dir400(self):
        return self.dir400
    @dir400.setter
    def dir400(self,value="Raghu400"):
        self.dir400 = value
    @property
    def dir160(self):
        return self.dir160
    @dir160.setter
    def dir160(self,value="Raghu160"):
        self.dir160 = value
    @property
    def img400(self):
        return self.img400
    @img400.setter
    def img400(self,value):
        self.img400 = value
    @property
    def img160(self):
        return self.img160
    @img160.setter
    def img160(self,value):
        self.img160 = value
    @property
    def desc2(self):
        return self.desc2
    @desc2.setter
    def desc2(self,value):
        self.desc2 = value
    @property
    def option(self):
        return self.option
    @option.setter
    def option(self,value=""):
        self.option = value
    @property
    def dir800(self):
        return self.dir800
    @dir800.setter
    def dir800(self,value="Raghu800"):
        self.dir800 = value
    @property
    def img800(self):
        return self.img800
    @img800.setter
    def img800(self,value):
        self.img800 = value
    @property
    def isUpdateAvailable(self):
		return self.isUpdateAvailable
    @isUpdateAvailable.setter
    def isUpdateAvailable(self,value):
		self.isUpdateAvailable = value