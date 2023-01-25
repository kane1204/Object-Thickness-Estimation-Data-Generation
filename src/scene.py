#  Create a scene class that has a model and a list of samples
import random
from src.model import Model
from src.frame import Frame
import pyvista as pv
import numpy as np
from math import dist


pv.global_theme.background = (135, 206, 235)
pv.global_theme.smooth_shading = True
pv.global_theme.anti_aliasing = 'fxaa'
pv.set_jupyter_backend('pythreejs')

class Scene:
    def __init__(self, model, no_of_frames, res) -> None:
        self.model = model
        self.no_of_frames = no_of_frames
        self.frames = []
        self.model_rotation = 180
        self.resolution = res
        self.show_edges = False

    def generate_frames(self):
        '''Generate a number of frames for the scene'''
        obj_mesh = pv.read(self.model.obj_path)
        # print(self.model)
        tex_path = self.model.get_texture(0)
        if tex_path is not None:
            obj_texture = pv.read_texture(tex_path)
        base_mesh = self.createBaseMesh(obj_mesh)
        obj_mesh.rotate_vector(vector=(0, 1, 0), angle=self.model_rotation, inplace=True)

        # Create camera and setup the camera position
        near_range = 0.3
        far_range = 40
        camera = pv.Camera()
        camera.position = (-5.0, 0.5, -4.5) # Default camera position will change
        camera.clipping_range = (near_range, far_range)

        
        pl = pv.Plotter(window_size=[self.resolution, self.resolution])
        # Assign Camera
        pl.camera = camera

        try:
            obj = pl.add_mesh(obj_mesh, show_edges=self.show_edges, texture=obj_texture)
        except :
            print("Textures Not Working!")
            obj = pl.add_mesh(obj_mesh, show_edges=self.show_edges)

        for x in range(self.no_of_frames):
            camera.position = self.randomizeCameraPosition()

            c_pos = camera.position
            plane = self.createPlaneFromFrustum(camera.view_frustum().copy())
            _, end_ray_pts = self.planeToGrid(plane, self.resolution)

            pl.screenshot()
            depth_img = pl.get_image_depth(fill_value=0)
            _ = pl.add_mesh(base_mesh,color='green')
            pl.ren_win.SetOffScreenRendering(5)
            img = pl.screenshot("result/moomoo.png",transparent_background=True, 
                                window_size=[self.resolution,int(self.resolution*pl.window_size[1]/pl.window_size[0])])

            # Get the thickness map
            thicc_map = np.zeros((self.resolution*self.resolution))
            for i in range(len(end_ray_pts.points)):
                # Calculate ray intersection of each point in the grid
                points, _ = obj_mesh.ray_trace(c_pos, end_ray_pts.points[i])
                in1, out1 = self.outRayFinder(points)
                thicc_map[i] = dist(in1, out1) if (not in1 is None) else 0

            thicc_map = np.flip(thicc_map.reshape(self.resolution, self.resolution))
            
            self.frames.append(Frame(img, depth_img, thicc_map, c_pos))




    def outRayFinder(self, pts):
        if len(pts) == 0:
            return None, None
        # Find the first element in pts that is differnt from pts[0] and return that point onelin
        if len(pts) > 2:
            points = np.array(pts)
            # Bug here with the idx bit
            # print(points.shape)
            check = np.where(np.isclose(points, points[0], )  != [True, True, True])
            # print(len(check[0])<2)
            if len(check[0]) < 2:
                return None, None
            idx = check[0][1]
            return pts[0], pts[idx]
        elif len(pts) == 2:
            return pts[0], pts[1]
        else:
            return None,None

    def createBaseMesh(self, mesh):
        # Add a thin box below the mesh
        bounds = mesh.bounds
        rnge = (bounds[1] - bounds[0], bounds[5] - bounds[4], bounds[3] - bounds[2]) # x z y
        # print(rnge)

        expand = 10
        height = rnge[2] * 0.05
        center = np.array(mesh.center)
        center -= [0, mesh.center[2] + (bounds[3] + (height/3 )) , 0]

        width = rnge[0] * (1 + expand)
        length = rnge[1] * (1 + expand)
        base_mesh = pv.Cube(center, width, height, length)
        # base_mesh.rotate_x(-90, inplace=True)
        return base_mesh

    def planeToGrid(self, frustum, n, center=None):
        # Find the center of the plane
        if center is not None:
            center = center
        else:
            center = frustum.center

        corners = frustum.points
        # Find the normal of the plane
        normal = np.cross(corners[1] - corners[0], corners[2] - corners[0])
        normal /= np.linalg.norm(normal)

        # Find the width and height of the plane
        width = dist(corners[0], corners[1])
        height = dist(corners[0], corners[3])

        # Create a grid of points that are evenly spaced
        grid = pv.Plane(center, normal, width, height, i_resolution=n-1, j_resolution=n-1)
        return grid, grid.ctp() # ctp = cell to point
    
    def createPlaneFromFrustum(self, frustum):
        # Furthest Frustum
        plane = frustum
        plane = plane.extract_points(1)
        plane = plane.extract_points(2)
        plane = plane.extract_points(3)
        return plane

    def randomizeCameraPosition(self):
        # Randomize the camera where
        # X can only be between 2 and 5 or -5 and -2
        # Y can only be between 2 and 10
        # Z can only be between 2 and 4.5 or -4.5 and -2
        
        x = random.uniform(2, 5) if random.randint(0, 1) == 0 else random.uniform(-5, -2)
        y = random.uniform(2, 10)
        z = random.uniform(2, 4.5) if random.randint(0, 1) == 0 else random.uniform(-4.5, -2)
        return (x, y, z)