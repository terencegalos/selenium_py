
class active_record:
    
    def __init__(self):
        self.container = []
        
    def __getitem__(self,position):
        return self.container[position]
        
    def __len__(self):
        return len(self.container)

    def __str__(self):
        print self.container
        
    @property
    def container(self):
        return self.container
        
    def save(self,obj):
        
        if isinstance(obj,list): #check if its a list
            for o in obj:
                if o is not None: #if img detected
                    #print type(o)
                    try:
						if o.sku not in [db.sku for db in self.container]: #check if there's a duplicate
							self.container.append(o)
                    except: #if list instance instead of tablegateways instance used
						if o[1] not in [db[1] for db in self.container]:
							self.container.append(o)

        else:
            if obj is not None: #if img detected
                if obj.sku not in [db.sku for db in self.container]:
                    self.container.append(obj) 