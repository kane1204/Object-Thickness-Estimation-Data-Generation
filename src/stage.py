# Create a stage class that handles an generates scenes
import tqdm
import pandas as pd

from src.scene import Scene

class Stage:
    def __init__(self, models, no_of_frames) -> None:
        self.models = models
        self.no_of_frames = no_of_frames
        self.df_cols = ['model_id', 'model_type', 'img', 'depth_map', 'thicc_map', 'cam_pos']
        self.data_frame = pd.DataFrame(columns=self.df_cols)
        
        self.image_res = 256
        self.scenes = []

    def generate_scene(self, model):
        '''Generate a scene with a number of frames and saves frames to the data frame'''
        scene = Scene(model, self.no_of_frames, self.image_res)
        scene.generate_frames()
        self.append_to_data_frame(scene)
        # Only append for testing could be memory intensive
        self.scenes.append(scene)
        # del scene

    def generate_scenes(self):
        '''Generate for each model a scene with a number of frames'''
        for model in tqdm.tqdm(self.models):
            self.generate_scene(model)
            # After every so many scenes, update the data frame to a csv file
            if len(self.data_frame) > 100:
                self.data_frame.to_csv('data.csv', index=False)
                self.data_frame = pd.DataFrame(columns=self.df_cols)

    
    def append_to_data_frame(self, scene):
        # frames is a list of frames also add the model name to the data frame
        for frame in scene.frames:
            self.data_frame = self.data_frame.append({'model_id': scene.model.model_id, 'model_type': scene.model.model_type, 'img': frame.imgs, 'depth_map': frame.depth_maps, 'thicc_map': frame.thicc_maps, 'cam_pos': frame.cam_pos}, ignore_index=True)