from src.model_loader import ModelLoader 
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from src.stage import Stage
from sys import platform
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
subset = models[508:-1]

stage = Stage(subset, 3, isWindows)
stage.generate_scenes()
