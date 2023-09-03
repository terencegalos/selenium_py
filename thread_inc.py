import threading

class thread_class():

    def __init__(self):
        self.queue = [] # active tasks
        self.threads = [] # active workers
        self.counter = 0 # desired worker count
        
    def threader(self,func,params,num):
        for param in params:
            self.queue[:-1] = [param] #worker holder
            print self.counter
            if self.counter == num or param == params[-1:]: #if num workers reached OR final batch
                for q in self.queue:
                    t = threading.Thread(target=func,args=(q,))
                    #t.daemon = True
                    self.threads.append(t)
                    t.start()
                    
                for thread in self.threads: #wait for the batch to finish
                    thread.join()
                    
                #reset counter and queue
                self.counter = 0
                del self.queue[:]
                del self.threads[:]
                #time.sleep(5)
            self.counter+=1