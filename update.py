from paraview.simple import *
import threading
import time


source=FindSource("LiveProgrammableSource1")


def update(): # This script update the reading of the data from the filter, as well as the displayed time by paraview every second. It is generating errors that do not make sense and should be ignored.
    starttime = time.time()
    while True:
        try:
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
            source.UpdatePipelineInformation()
        except:
            pass


try:
    t1 = threading.Thread(target=update, args=())
    t1.start()
except:
    pass

### exec(open("./update.py").read())