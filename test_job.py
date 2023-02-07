from src.model_loader import ModelLoader 
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from src.stage import Stage
from sys import platform
DATA_ROOT_LINUX = "data/shapenet_samples"
DATA_ROOT_WINDOWS = "data\\shapenet_samples"
isWindows = False

if  platform == "linux":
    print("On Linux!")
    # Linux
    data = ModelLoader(DATA_ROOT_LINUX, False , False)

elif platform == "win32":
    print("On Windows!")
    isWindows = True
    # Windows
    data = ModelLoader(DATA_ROOT_WINDOWS, False , True)
else:
    print("Unknown OS!")
    exit(1)

# Create a list of models
models = data.get_models("02828884")

subset = models[0:2]

stage = Stage(subset, 1, isWindows)
stage.generate_scenes()