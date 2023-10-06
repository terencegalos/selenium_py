
class ActiveRecord:
    
    def __init__(self):
        self._container = []
        
    def __getitem__(self,position):
        return self._container[position]
        
    def __len__(self):
        return len(self._container)

    def __str__(self):
        print(self._container)
    
    def _add(self,obj):
        if obj.sku not in [db.sku for db in self._container]:
            self._container.append(obj)
        
    @property
    def container(self):
        return self._container
    
    @container.setter
    def container(self,value):
        self._container = value
        
    def save(self,obj):
        print(obj)
        
        # if isinstance(obj,list): #check if its a list
        #     print obj
        #     for o in obj:
        #         if o is not None: #if img detected
        #             print type(o)
        #             self._add(o)

        # else:
        if obj is not None: #check if available img
            self._add(obj)