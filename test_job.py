from src.model_loader import ModelLoader 
import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt
from src.stage import Stage
# Linux
DATA_ROOT_LINUX = "data/shapenet_samples"
data = ModelLoader(DATA_ROOT_LINUX, False , False)
# Create a list of models
models = data.get_models("02828884")

subset = models[0:100]

stage = Stage(subset, 3)
stage.generate_scenes()

# Windows
# DATA_ROOT_WINDOWS = "data\\shapenet_samples"
# data = ModelLoader(DATA_ROOT_WINDOWS, False , True)
# # Create a list of models
# models = data.get_models("02828884")

# subset = models[0:100]

# stage = Stage(subset, 3)
# stage.generate_scenes()