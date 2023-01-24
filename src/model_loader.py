import pyvista as pv
from tqdm import tqdm
from src.model import Model 
import os
class ModelLoader:
    def __init__(self, data_root):
        self.data_root = data_root
        # Map model paths from catagory to model path
        self.model_paths = {}

        for catagory in tqdm(os.listdir(data_root), desc='Loading Models'):
            catagory_path = os.path.join(data_root, catagory)
            model_p = []
            for model in os.listdir(catagory_path):
                model_path = os.path.join(catagory_path, model)
                model_p.append(Model(model_path))
            self.model_paths[catagory] = model_p

    def get_model_paths(self):
        return self.model_paths

    def get_model_paths_by_catagory(self, catagory):
        return self.model_paths[catagory]

    def get_model_paths_by_catagory_and_model(self, catagory, model):
        return self.model_paths[catagory][model]

    def get_models(self, catagory):
        return self.model_paths[catagory]

