from src.model_loader import ModelLoader 
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from src.stage import Stage
from sys import platform
import os
import sys
DATA_ROOT_LINUX = "data/ShapeNetCoreJK_Segment"
DATA_ROOT_WINDOWS = "data\\ShapeNetCoreJK_Segment"
isWindows = False

if  platform == "linux":
    print("On Linux!")
    # Linux
    data = ModelLoader(DATA_ROOT_LINUX, True , False)

elif platform == "win32":
    print("On Windows!")
    isWindows = True
    # Windows
    data = ModelLoader(DATA_ROOT_WINDOWS, False , True)
else:
    print("Unknown OS!")
    exit(1)

# Create a list of models
models = data.get_all_models()
# https://machinelearningmastery.com/how-to-save-a-numpy-array-to-file-for-machine-learning/ do this
subset = models[1534:-1]

stage = Stage(subset, 3, isWindows)
try:
    stage.generate_scenes()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()  # this is to get error line number and description.
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]  # to get File Name.
    error_string="ERROR : Error Msg:{},File Name : {}, Line no : {}\n".format(e,file_name,exc_tb.tb_lineno)
    file_log = open("error_log.log", "a")
    file_log.write(error_string)
    file_log.close()
