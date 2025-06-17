import pygame

from glapp.Utils import create_program
from glapp.PyOGLApp import *
from glapp.Material import *

# from glapp.Cube import *
from glapp.LoadMesh import *
from glapp.Light import *
from glapp.Axes import *


# from glApp.MovingCube import *


class WolfShader(PyOGLApp):
    def __init__(self):
        super().__init__(850, 200, 1000, 600)
        self.floor = None
        self.tabletop = None
        self.lights = []
        self.axes = None
        self.wolf = None
        glEnable(GL_CULL_FACE)

    def initialise(self):
        mat = Material("shaders/texturedvert.vs", "shaders/texturedfrag.vs")
        axesmat = Material("shaders/vertexcolvert.vs", "shaders/vertexcolfrag.vs")
        # self.program_id = mat.program_id

        self.axes = Axes(pygame.Vector3(0, 0, 0), axesmat)

        self.wolf = LoadMesh("models/wolf.obj", "images/gold.png",  # draw_type=GL_POLYGON,
                             location=pygame.Vector3(0, 0, 0),
                             scale=pygame.Vector3(0.2, 0.2, 0.2),
                             move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)),
                             material=mat)

        self.lights.append(Light(pygame.Vector3(-1, 1, 0), pygame.Vector3(1, 1, 1), 0))
        # self.lights.append(Light3(pygame.Vector3(1, 1, 0), pygame.Vector3(1, 0, 1), 1))
        self.camera = Camera(self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def camera_init(self):
        pass

    def display(self):
        # glLineWidth(10)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # glUseProgram(self.program_id)
        # self.camera.update()
        # self.light.update()
        self.axes.draw(self.camera, self.lights)

        self.wolf.draw(self.camera, self.lights)

        # glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)


WolfShader().mainloop()
