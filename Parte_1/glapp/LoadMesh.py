from OpenGL.GL import *
import pygame
from glapp.Mesh import Mesh

from glapp.MovingMesh import MovingMesh
from glapp.Transformation import Rotation
from glapp.Utils import *


class LoadMesh(MovingMesh):
    def __init__(self, filename,imagefile, program_id, draw_type=GL_TRIANGLES,
                 location=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1)
                 ):
        self.filename = filename
        # coordinates, triangles = self.load_drawing(filename)
        coordinates, triangles, squares, uvs, uvs_ind, normals, normal_ind = self.load_drawing(filename)
        # vertices= format_vertices(coordinates,triangles)
        vertices = format_vertices2(coordinates, triangles, squares)
        vertex_normals = format_vertices3(normals, normal_ind)
        vertex_uvs = format_vertices3(uvs, uvs_ind)
        #vertex_uvs=[]
        colors = []
        for i in range(len(vertices)):
            # colors.append(random.random())
            # colors.append(random.random())
            # colors.append(random.random())
            colors.append(1)
            colors.append(1)
            colors.append(1)
        super().__init__(program_id, vertices,imagefile, vertex_normals, vertex_uvs, colors, draw_type, location, rotation, scale,
                         move_rotation=move_rotation, move_translate=move_translate, move_scale=move_scale)

    def load_drawing(self, filename):
        vertices = []
        triangles = []
        squares = []
        normals = []
        normal_ind = []
        uvs = []
        uvs_ind = []
        with open(filename) as fp:
            line = fp.readline()
            while line:

                if line[:2] == "v ":
                    vx, vy, vz = [float(value) for value in line[2:].split()]
                    vertices.append((vx, vy, vz))
                if line[:2] == "vn":
                    vx, vy, vz = [float(value) for value in line[3:].split()]
                    normals.append((vx, vy, vz))
                if line[:2] == "vt":
                    if len(line[3:].split()) == 2:
                        vx, vy = [float(value) for value in line[3:].split()]
                        uvs.append((vx, vy))
                    elif len(line[3:].split()) == 3:
                        vx, vy, vz = [float(value) for value in line[3:].split()]
                        uvs.append((vx, vy, vz))
                if line[:2] == "f ":
                    if (len(line[2:].split()) == 3):
                        t1, t2, t3 = [value for value in line[2:].split()]
                        t1 = t1.replace("//", "/")
                        t2 = t2.replace("//", "/")
                        t3 = t3.replace("//", "/")
                        triangles.append([int(value) for value in t1.split('/')][0] - 1)
                        triangles.append([int(value) for value in t2.split('/')][0] - 1)
                        triangles.append([int(value) for value in t3.split('/')][0] - 1)
                        uvs_ind.append([int(value) for value in t1.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t2.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t3.split('/')][1] - 1)
                        if (len(t1.split('/')) == 3):
                            normal_ind.append([int(value) for value in t1.split('/')][2] - 1)
                            normal_ind.append([int(value) for value in t2.split('/')][2] - 1)
                            normal_ind.append([int(value) for value in t3.split('/')][2] - 1)
                    elif (len(line[2:].split()) == 4):
                        t1, t2, t3, t4 = [value for value in line[2:].split()]
                        t1 = t1.replace("//", "/")
                        t2 = t2.replace("//", "/")
                        t3 = t3.replace("//", "/")
                        t4 = t4.replace("//", "/")
                        squares.append([int(value) for value in t1.split('/')][0] - 1)
                        squares.append([int(value) for value in t2.split('/')][0] - 1)
                        squares.append([int(value) for value in t3.split('/')][0] - 1)
                        squares.append([int(value) for value in t4.split('/')][0] - 1)
                        uvs_ind.append([int(value) for value in t1.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t2.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t3.split('/')][1] - 1)
                        uvs_ind.append([int(value) for value in t4.split('/')][1] - 1)
                        if(len(t1.split('/'))==3):
                            normal_ind.append([int(value) for value in t1.split('/')][2] - 1)
                            normal_ind.append([int(value) for value in t2.split('/')][2] - 1)
                            normal_ind.append([int(value) for value in t3.split('/')][2] - 1)
                            normal_ind.append([int(value) for value in t4.split('/')][2] - 1)
                line = fp.readline()
        # return vertices,triangles       #,squares
        return vertices, triangles, squares, uvs, uvs_ind, normals, normal_ind
