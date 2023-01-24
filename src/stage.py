# Create a stage class that handles an generates scenes
import tqdm
import pandas as pd

from scene import Scene

class Stage:
    def __init__(self, models, no_of_frames) -> None:
        self.models = models
        self.no_of_frames = no_of_frames
        self.data_frame = pd.DataFrame()
        self.image_res = 256

    def generate_scene(self, model):
        '''Generate a scene with a number of frames and saves frames to the data frame'''
        scene = Scene(model, self.no_of_frames, self.image_res)
        scene.generate_samples()
        self.data_frame = self.data_frame.append(scene.frames)
        del scene

    def generate_scenes(self):
        '''Generate for each model a scene with a number of frames'''
        for model in tqdm.tqdm(self.models):
            self.generate_scene(model)
            # After every so many scenes, update the data frame to a csv file
            if len(self.data_frame) > 100:
                self.data_frame.to_csv('data.csv', index=False)
                self.data_frame = pd.DataFrame()

    
