import pygame

from glapp.Utils import create_program
from glapp.PyOGLApp import *
from glapp.Material import *

# from glapp.Cube import *
from glapp.LoadMesh import *
from glapp.Light import *
from glapp.Axes import *


# from glApp.MovingCube import *


class TexturedObjects(PyOGLApp):
    def __init__(self):
        super().__init__(850, 200, 1000, 600)
        self.floor = None
        self.tabletop = None
        self.lights = []
        self.axes=None
        self.teapot=None
        self.donut=None
        self.granny=None
        self.wolf=None
        glEnable(GL_CULL_FACE)

    def initialise(self):
        mat = Material("shaders/texturedvert.vs", "shaders/texturedfrag.vs")
        axesmat = Material("shaders/vertexcolvert.vs", "shaders/vertexcolfrag.vs")
        # self.program_id = mat.program_id

        self.axes = Axes(pygame.Vector3(0, 0, 0), axesmat)

        self.floor = LoadMesh("models/plane.obj", "images/tiles.png",
                              location=pygame.Vector3(0, -1.5, 0),
                              scale=pygame.Vector3(5, 1, 5),
                              material=mat)
        self.granny = LoadMesh("models/granny.obj", "images/timber.png",
                                 location=pygame.Vector3(-1.5, -1.5, 0),
                                 scale=pygame.Vector3(0.02,0.02,0.02),
                                 material=mat)
        self.tabletop = LoadMesh("models/tabletop.obj", "images/timber.png",
                                 location=pygame.Vector3(0, -0.5, 0),
                                 scale=pygame.Vector3(1.2, 0.8, 1.2),
                                 material=mat)
        self.teapot = LoadMesh("models/teapot.obj", "images/square_tex.jpg",
                                 location=pygame.Vector3(0.5,  -0.5, 0),
                                 scale=pygame.Vector3(0.2, 0.2, 0.2),
                                 material=mat)
        self.donut = LoadMesh("models/donut.obj", "images/dona.jpg" , #draw_type=GL_POLYGON,
                               location=pygame.Vector3(-0.4, -0.2, 0),
                               scale=pygame.Vector3(0.2, 0.2, 0.2),
                               material=mat)

        self.leg1 = LoadMesh("models/tableleg.obj", "images/timber.png",
                             location=pygame.Vector3(-0.5, -1, 0.5),
                             material=mat)
        self.leg2 = LoadMesh("models/tableleg.obj", "images/timber.png",
                             location=pygame.Vector3(-0.5, -1, -0.5),
                             material=mat)
        self.leg3 = LoadMesh("models/tableleg.obj", "images/timber.png",
                             location=pygame.Vector3(0.5, -1, - 0.5),
                             material=mat)
        self.leg4 = LoadMesh("models/tableleg.obj", "images/timber.png",
                             location=pygame.Vector3(0.5, -1, 0.5),
                             material=mat)

        self.lights.append(Light(pygame.Vector3(-2, 2, 0), pygame.Vector3(1, 1, 1), 0))
        #self.lights.append(Light3(pygame.Vector3(1, 1, 0), pygame.Vector3(1, 0, 1), 1))
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
        self.tabletop.draw(self.camera, self.lights)
        self.leg1.draw(self.camera, self.lights)
        self.leg2.draw(self.camera, self.lights)
        self.leg3.draw(self.camera, self.lights)
        self.leg4.draw(self.camera, self.lights)

        self.floor.draw(self.camera, self.lights)
        self.granny.draw(self.camera, self.lights)
        self.teapot.draw(self.camera,self.lights)
        self.donut.draw(self.camera,self.lights)

        # glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)


TexturedObjects().mainloop()
