from OpenGL.GL import *
import pygame

from glapp.Graphics_Data import Graphics_Data
from glapp.Texture import Texture
from glapp.Transformation import *
from glapp.Uniform import Uniform


class MovingMesh:
    def __init__(self, program_id, vertices, imagefile, vertex_normals,vertex_uvs,vertex_colors, draw_type,
                 translation=pygame.Vector3(0,0,0),
                 rotation=Rotation(0,pygame.Vector3(0,1,0)),
                 scale=pygame.Vector3(1,1,1),
                 move_rotation=Rotation(0,pygame.Vector3(0,1,0)),
                 move_translate=pygame.Vector3(0,0,0),
                 move_scale=pygame.Vector3(1,1,1)
                 ):
        self.vertices = vertices
        self.vertex_normals=vertex_normals
        self.vertex_uvs=vertex_uvs
        self.draw_type = draw_type
        self.vao_ref = glGenVertexArrays(1)
        glBindVertexArray(self.vao_ref)
        position = Graphics_Data("vec3", self.vertices)
        position.create_variable(program_id, "position")
        colors = Graphics_Data("vec3", vertex_colors)
        colors.create_variable(program_id, "vertex_color")

        v_normals = Graphics_Data("vec3", vertex_normals)
        v_normals.create_variable(program_id, "vertex_normal")

        v_uvs = Graphics_Data("vec2", vertex_uvs)
        v_uvs.create_variable(program_id, "vertex_uv")

        self.transformation_mat=identity_matrix()

        self.transformation_mat=rotateA(self.transformation_mat,rotation.angle,rotation.axis)

        self.transformation_mat=translate(self.transformation_mat,translation.x,translation.y,translation.z)

        self.transformation_mat=scale3(self.transformation_mat, scale.x,scale.y,scale.z)

        self.transformation=Uniform("mat4",self.transformation_mat)
        self.transformation.find_variable(program_id,"model_mat")

        self.move_rotation=move_rotation
        self.move_translate=move_translate
        self.move_scale=move_scale

        self.program_id = program_id

        self.image=Texture(imagefile)
        self.texture=Uniform("sampler2D",[self.image.texture_id,1])
        self.texture.find_variable(program_id,"tex")

    def draw(self):
        self.texture.load()
        self.transformation_mat = rotateA(self.transformation_mat, self.move_rotation.angle, self.move_rotation.axis)
        self.transformation_mat = translate(self.transformation_mat, self.move_translate.x, self.move_translate.y, self.move_translate.z)
        self.transformation_mat = scale3(self.transformation_mat, self.move_scale.x, self.move_scale.y, self.move_scale.z)
        self.transformation = Uniform("mat4", self.transformation_mat)
        self.transformation.find_variable(self.program_id, "model_mat")
        self.transformation.load()
        glBindVertexArray(self.vao_ref)
        glDrawArrays(self.draw_type, 0, len(self.vertices))
