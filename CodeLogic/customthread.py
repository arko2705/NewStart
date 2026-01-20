from threading import Thread

from newstartapp.models import ProcessKeeper
class returningThread(Thread):
   
    def __init__(self,group=None,target=None,name=None,args=(),kwargs={}):
        Thread.__init__(self,group,target,name,args,kwargs)
        self._returnit=None
    def run(self):
        if self._target is not None:  
            self._returnit=self._target(*self._args,**self._kwargs)
    def join(self, timeout = None):
        Thread.join(self)
        return self._returnit
