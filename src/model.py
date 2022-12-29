import os

class Model:
    def __init__(self, model_path):
        self.model_path = model_path
        self.obj_path = model_path + "\\model.obj"
        self.mtl_path = model_path + "\\model.mtl"
        # Append all textures to a list within image folder
        self.textures = []
        # Error handle if no images folder
        try:
            for file in os.listdir(model_path + "\\images"):
                if file.endswith(".jpg"):
                    self.textures.append(model_path + "\\images\\" + file)
                elif file.endswith(".png"):
                    self.textures.append(model_path + "\\images\\" + file)
        except:
            pass

    def get_model_path(self):
        return self.model_path
    
    def get_obj_path(self):
        return self.obj_path

    def get_mtl_path(self):
        return self.mtl_path

    def get_textures(self):
        return self.textures

    def get_texture(self, index):
        if len(self.textures) == 0:
            return None
        else:
            return self.textures[index]
