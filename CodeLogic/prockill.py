import psutil
import os
from newstartapp.models import ProcessKeeper
import signal
def currProc():
    my_pid = os.getpid()
    for proc in psutil.process_iter():
        try:
            processID = proc.pid
            if processID == my_pid:
                return processID
        except:
            pass
    return
def killer():
    ids=ProcessKeeper.objects.values_list('procID', flat=True)
    for procId in ids:
        try:
            os.kill(procId,signal.SIGTERM)
        except:
            pass
    return
if __name__=="__main__":
    killer()
