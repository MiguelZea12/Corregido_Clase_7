import pygame
from pygame.locals import *
from .Camera import *
import os
from OpenGL.GL import *
from OpenGL.GLU import *


class PyOGLApp():
    def __init__(self, screenposX, screenposY, screen_width, screen_height):
        #os.environ['SDL_VIDEO_WINDOWS_POS'] = "%d,%d" % (screenposX, screenposY)
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        self.screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('OpenGL in Python')
        self.camera = None
        self.program_id = None

        self.clock=pygame.time.Clock()


    def initialise(self):
        pass

    def display(self):
        pass

    def camera_init(self):
        pass

    def main_loop(self):
        done = False
        self.initialise()
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.mouse.set_visible(True)
                        pygame.event.set_grab(False)
                    if event.key == K_SPACE:
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
            self.camera_init()
            self.display()
            pygame.display.flip()

            self.clock.tick(60)
            # pygame.time.wait(100);
        pygame.quit()
