class Frame:
    def __init__(self, img, d_map, t_map, c_pos):
        self.imgs = img
        self.depth_maps = d_map
        self.thicc_maps = t_map
        self.cam_pos = c_pos
        