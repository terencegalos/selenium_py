
class active_record:
    
    def __init__(self):
        self.container = []
        
    def __getitem__(self,position):
        return self.container[position]
        
    def __len__(self):
        return len(self.container)

    def __str__(self):
        print self.container
    
    def _add(self,obj):
        if obj.sku not in [db.sku for db in self.container]:
            self.container.append(obj)
        
    @property
    def container(self):
        return self.container
        
    def save(self,obj):
        
        if isinstance(obj,list): #check if its a list
            for o in obj:
                if o is not None: #if img detected
                    # print type(o)
                    self._add(o)

        else:
            if obj is not None: #if img detected
                self._add(obj)