import threading
import os
import glob
import pandas as pd
import shutil

filelist = glob.glob('csv0/particles_positions_0_t*.parquet'.format(str(0)))

print(filelist)
