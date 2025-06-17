import random

from OpenGL.GL import *

from .Utils import format_vertices, format_vertices3, format_vertices2
from .Mesh import *
import pygame
import random

from .Mesh import Mesh


class LoadMesh(Mesh):

    def __init__(self, filename, imagefile, draw_type=GL_TRIANGLES, location=pygame.Vector3(0, 0, 0),
                 rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 scale=pygame.Vector3(1, 1, 1),
                 move_rotation=Rotation(0, pygame.Vector3(0, 1, 0)),
                 move_translate=pygame.Vector3(0, 0, 0),
                 move_scale=pygame.Vector3(1, 1, 1),
                 material=None
                 ):

        coordinates, triangles, squares, uvs, uvs_ind, normals, normal_ind = self.load_drawing(filename)
        vertices = format_vertices2(coordinates, triangles, squares)
        vertex_normals = format_vertices3(normals, normal_ind) if normals and normal_ind else []
        vertex_uvs = format_vertices3(uvs, uvs_ind) if uvs and uvs_ind else []
        colors = []
        for i in range(len(vertices)):
            colors.append(1)
            colors.append(1)
            colors.append(1)
        super().__init__(vertices, imagefile=imagefile,
                         vertex_normals=vertex_normals, vertex_uvs=vertex_uvs,
                         vertex_colors=colors, draw_type=draw_type, translation=location, rotation=rotation,
                         scale=scale,
                         move_rotation=move_rotation, move_translate=move_translate, move_scale=move_scale,
                         material=material)

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
                        
                        # Agregar índices de vértices
                        triangles.append([int(value) for value in t1.split('/')][0] - 1)
                        triangles.append([int(value) for value in t2.split('/')][0] - 1)
                        triangles.append([int(value) for value in t3.split('/')][0] - 1)
                        
                        # Agregar índices de UV solo si existen
                        t1_parts = t1.split('/')
                        t2_parts = t2.split('/')
                        t3_parts = t3.split('/')
                        
                        if len(t1_parts) > 1 and t1_parts[1] and len(t2_parts) > 1 and t2_parts[1] and len(t3_parts) > 1 and t3_parts[1]:
                            try:
                                uv1 = int(t1_parts[1]) - 1
                                uv2 = int(t2_parts[1]) - 1
                                uv3 = int(t3_parts[1]) - 1
                                
                                # Verificar que los índices sean válidos
                                if 0 <= uv1 < len(uvs) and 0 <= uv2 < len(uvs) and 0 <= uv3 < len(uvs):
                                    uvs_ind.append(uv1)
                                    uvs_ind.append(uv2)
                                    uvs_ind.append(uv3)
                            except (ValueError, IndexError):
                                pass  # Ignorar si no se pueden convertir a enteros
                        
                        # Agregar índices de normales solo si existen
                        if len(t1_parts) == 3 and t1_parts[2] and len(t2_parts) == 3 and t2_parts[2] and len(t3_parts) == 3 and t3_parts[2]:
                            try:
                                n1 = int(t1_parts[2]) - 1
                                n2 = int(t2_parts[2]) - 1
                                n3 = int(t3_parts[2]) - 1
                                
                                # Verificar que los índices sean válidos
                                if 0 <= n1 < len(normals) and 0 <= n2 < len(normals) and 0 <= n3 < len(normals):
                                    normal_ind.append(n1)
                                    normal_ind.append(n2)
                                    normal_ind.append(n3)
                            except (ValueError, IndexError):
                                pass  # Ignorar si no se pueden convertir a enteros
                                
                    elif (len(line[2:].split()) == 4):
                        t1, t2, t3, t4 = [value for value in line[2:].split()]
                        t1 = t1.replace("//", "/")
                        t2 = t2.replace("//", "/")
                        t3 = t3.replace("//", "/")
                        t4 = t4.replace("//", "/")
                        
                        # Agregar índices de vértices
                        squares.append([int(value) for value in t1.split('/')][0] - 1)
                        squares.append([int(value) for value in t2.split('/')][0] - 1)
                        squares.append([int(value) for value in t3.split('/')][0] - 1)
                        squares.append([int(value) for value in t4.split('/')][0] - 1)
                        
                        # Agregar índices de UV solo si existen
                        t1_parts = t1.split('/')
                        t2_parts = t2.split('/')
                        t3_parts = t3.split('/')
                        t4_parts = t4.split('/')
                        
                        if (len(t1_parts) > 1 and t1_parts[1] and len(t2_parts) > 1 and t2_parts[1] and 
                            len(t3_parts) > 1 and t3_parts[1] and len(t4_parts) > 1 and t4_parts[1]):
                            try:
                                uv1 = int(t1_parts[1]) - 1
                                uv2 = int(t2_parts[1]) - 1
                                uv3 = int(t3_parts[1]) - 1
                                uv4 = int(t4_parts[1]) - 1
                                
                                # Verificar que los índices sean válidos
                                if (0 <= uv1 < len(uvs) and 0 <= uv2 < len(uvs) and 
                                    0 <= uv3 < len(uvs) and 0 <= uv4 < len(uvs)):
                                    uvs_ind.append(uv1)
                                    uvs_ind.append(uv2)
                                    uvs_ind.append(uv3)
                                    uvs_ind.append(uv4)
                            except (ValueError, IndexError):
                                pass  # Ignorar si no se pueden convertir a enteros
                        
                        # Agregar índices de normales solo si existen
                        if (len(t1_parts) == 3 and t1_parts[2] and len(t2_parts) == 3 and t2_parts[2] and 
                            len(t3_parts) == 3 and t3_parts[2] and len(t4_parts) == 3 and t4_parts[2]):
                            try:
                                n1 = int(t1_parts[2]) - 1
                                n2 = int(t2_parts[2]) - 1
                                n3 = int(t3_parts[2]) - 1
                                n4 = int(t4_parts[2]) - 1
                                
                                # Verificar que los índices sean válidos
                                if (0 <= n1 < len(normals) and 0 <= n2 < len(normals) and 
                                    0 <= n3 < len(normals) and 0 <= n4 < len(normals)):
                                    normal_ind.append(n1)
                                    normal_ind.append(n2)
                                    normal_ind.append(n3)
                                    normal_ind.append(n4)
                            except (ValueError, IndexError):
                                pass  # Ignorar si no se pueden convertir a enteros
                                
                line = fp.readline()
        return vertices, triangles, squares, uvs, uvs_ind, normals, normal_ind