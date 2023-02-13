# Create a stage class that handles an generates scenes
import tqdm
import pandas as pd
from datetime import datetime
from src.scene import Scene
import os

class Stage:
    def __init__(self, models, no_of_frames, isWindows) -> None:
        self.models = models
        self.no_of_frames = no_of_frames
        self.df_cols = ['model_id', 'model_type', 'img', 'depth_map', 'thicc_map', 'cam_pos']
        self.df_dict = {'model_id': str, 'model_type': str, 'img': object, 'depth_map': object, 'thicc_map':  object, 'cam_pos': object}
        self.data_frame = pd.DataFrame(columns=self.df_cols).astype(self.df_dict)
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.root_folder = f"gen_data_{now}"
        self.image_res = 128
        self.isWindows = isWindows
        # self.scenes = []
        print(f"Creating root folder: {self.root_folder}/")
        os.mkdir(self.root_folder)

    def generate_scene(self, model, model_folder):
        '''Generate a scene with a number of frames and saves frames to the data frame'''
        scene = Scene(model, self.no_of_frames, self.image_res, self.isWindows, model_folder, self.root_folder)
        scene.generate_frames()
        # self.append_to_data_frame(scene)
        # Only append for testing could be memory intensive
        # self.scenes.append(scene)
        del scene

    def generate_scenes(self):
        '''Generate for each model a scene with a number of frames'''
        print("Start Generating Scenes!")
        iter = 0
        with tqdm.tqdm(self.models) as t:
            for model in t:
                rate = t.format_dict["rate"]
                remaining = (t.total - t.n) if rate and t.total else 0
            # for model in tqdm.tqdm(self.models):
                trackerfile = open(os.path.join(self.root_folder,"tracker.txt"), "a")  # append mode
                trackerfile.write(f"Model: {iter}-{datetime.now()}, Samples Remaining: {remaining}, \n")
                trackerfile.close()
                # Create Directory Structure
                model_folder = os.path.join(self.root_folder, model.model_type,model.model_id)
                os.makedirs(model_folder, exist_ok=True)

                self.generate_scene(model, model_folder)
                iter += 1

        print(f"Finished and saved to : {self.root_folder} !")
    
    def append_to_data_frame(self, scene):
        # frames is a list of frames also add the model name to the data frame
        for frame in scene.frames:
            self.data_frame = self.data_frame.append({'model_id': scene.model.model_id, 'model_type': scene.model.model_type, 'img': frame.imgs.tolist(), 'depth_map': frame.depth_maps.tolist(), 'thicc_map': frame.thicc_maps.tolist(), 'cam_pos': frame.cam_pos}, ignore_index=True)
