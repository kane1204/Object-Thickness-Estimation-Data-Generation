class Frame:
    def __init__(self, img, d_map, t_map, c_pos):
        self.img = img
        self.depth_map = d_map
        self.thicc_map = t_map
        self.cam_pos = c_pos
    def __str__(self) -> str:
        return f"Frame: {self.img.shape}, {self.depth_map.shape}, {self.thicc_map.shape}, {self.cam_pos.shape}"
        