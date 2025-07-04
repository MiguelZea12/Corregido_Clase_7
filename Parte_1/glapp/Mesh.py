from OpenGL.GL import *
import pygame

from glapp.Graphics_Data import Graphics_Data
from glapp.Transformation import *
from glapp.Uniform import Uniform


class Mesh:
    def __init__(self, program_id, vertices, vertex_colors, draw_type,
                 translation=pygame.Vector3(0,0,0),
                 rotation=Rotation(0,pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1)):
        self.vertices = vertices

        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        position = Graphics_Data("vec3", self.vertices)
        position.create_variable(program_id, "position")
        colors = Graphics_Data("vec3", vertex_colors)
        colors.create_variable(program_id, "vertex_color")
        self.transformation_mat=identity_matrix()

        self.transformation_mat=rotateA(self.transformation_mat,rotation.angle,rotation.axis)

        self.transformation_mat=translate(self.transformation_mat,translation.x,translation.y,translation.z)

        self.transformation_mat=scale3(self.transformation_mat, scale.x,scale.y,scale.z)

        self.transformation=Uniform("mat4",self.transformation_mat)
        self.transformation.find_variable(program_id,"model_mat")

        self.program_id = program_id

    def draw(self):
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
