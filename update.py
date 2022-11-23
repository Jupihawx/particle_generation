from paraview.simple import *
import threading
import time


source=FindSource("LiveProgrammableSource1")


def update():
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