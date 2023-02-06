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

subset = [models[3],models[4],models[5],models[6],models[7],models[8],models[9],models[10],models[11],models[12],models[13],models[14]]

stage = Stage(subset, 3)
stage.generate_scenes()