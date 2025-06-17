import pygame

from glapp.Axes import Axes
from glapp.Cube import Cube
from glapp.MovingCube import MovingCube
from glapp.PyOGLApp import *
import numpy as np
from glapp.Utils import *

from glapp.LoadMesh import *

vertex_shader = r'''
#version 330 core

in vec3 position;
in vec3 vertex_color;

in vec3 vertex_normal;


uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;

out vec3 normal;
out vec3 fragpos;
out vec3 light_pos;
out vec3 view_pos;

void main() {

    light_pos= vec3(5,5,5);
    view_pos=vec3(inverse(model_mat) * 
                    vec4(view_mat[3][0],view_mat[3][1],view_mat[3][2],1));
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position, 1.0);
    normal= mat3(transpose(inverse(model_mat))) * vertex_normal;
    fragpos=vec3(model_mat * vec4(position, 1.0));
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core

in vec3 color;

in vec3 normal;
in vec3 fragpos;
in vec3 light_pos;
in vec3 view_pos;
out vec4 fragColor;
void main() {
    
    vec3 light_color = vec3(1,0,0);
    
    //ambient
    float a_strength=0.1;
    vec3 ambient=a_strength * light_color;
    
    //diffuse
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - fragpos);
    float diff = max(dot(norm,light_dir),0);
    vec3 diffuse = diff * light_color;
    
    //specular
    float s_strength=0.8;
    vec3 view_dir=normalize(view_pos - fragpos);    
    vec3 reflect_dir= normalize(-light_dir - norm);
    float spec= pow(max(dot(view_dir, reflect_dir), 0), 32);
    vec3 specular= s_strength * spec * light_color;
    
    fragColor = vec4(color * (ambient + diffuse + specular), 1.0f);
}
'''


class ShadedObjects(PyOGLApp):
    def __init__(self):
        super().__init__(850, 200, 1000, 600)

        self.axes = None
        self.moving_cube = None
        self.teapot = None
        self.teapot0 = None
        self.wolf = None
        self.ferrari = None
        self.ironman = None

    def initialise(self):
        self.program_id = create_program(vertex_shader, fragment_shader)
        # self.square = Square(self.program_id, pygame.Vector3(-0.5, 0.5, 0.0))
        # self.triangle = Triangle(self.program_id, pygame.Vector3(0.5, -0.5, 0.0))
        # self.axes = Axes(self.program_id, pygame.Vector3(0.0, 0.0, 0.0))
        # self.moving_cube = MovingCube(self.program_id,
        #                             location=pygame.Vector3(2, 1, 2),
        #                            move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)))
        # self.teapot0 = LoadMesh("models/teapot.obj", self.program_id,
        #                       #move_scale=pygame.Vector3(1.1,1.1,1.1)
        #                      )
        self.teapot = LoadMesh("models/teapot.obj", self.program_id,
                               location=pygame.Vector3(3, 3, 0),
                               move_rotation=Rotation(1, pygame.Vector3(0, 1, 0)),
                               # move_scale=pygame.Vector3(0.1,0,0)
                               )
        self.wolf = LoadMesh("models/wolf.obj", self.program_id,
                             location=pygame.Vector3(-6, -3, 0),
                             scale=pygame.Vector3(5, 5, 5),
                             move_rotation=Rotation(1, pygame.Vector3(0, 1, 2)))
        self.ferrari = LoadMesh("models/ferrari.obj", self.program_id,
                                location=pygame.Vector3(-3, -2, 0),
                                scale=pygame.Vector3(0.4, 0.4, 0.4),
                                # move_rotation=Rotation(2, pygame.Vector3(1, 1, 0))
                                )
        self.ironman = LoadMesh("models/IronMan.obj", self.program_id,
                                location=pygame.Vector3(-3, -2, 0),
                                scale=pygame.Vector3(0.4, 0.4, 0.4),
                                # move_rotation=Rotation(2, pygame.Vector3(1, 1, 0))
                                )
        self.camera = Camera(self.program_id, self.screen_width, self.screen_height)
        glEnable(GL_DEPTH_TEST)

    def camera_init(self):
        pass

    def display(self):
        # glLineWidth(10)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.program_id)
        self.camera.update()
        # self.square.draw()
        # self.triangle.draw()
        # self.axes.draw()
        # self.moving_cube.draw()
        # self.teapot0.draw()
        self.teapot.draw()
        #self.wolf.draw()
        #self.ironman.draw()
        # self.ferrari.draw()
        # glDrawArrays(GL_LINE_LOOP, 0, self.vertex_count)


ShadedObjects().main_loop()
