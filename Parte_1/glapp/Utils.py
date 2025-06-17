import numpy as np
from OpenGL.GL import *


def format_vertices(coordinates, triangles):
    allTriangles = []
    for t in range(0, len(triangles), 3):
        allTriangles.append(coordinates[triangles[t]])
        allTriangles.append(coordinates[triangles[t + 1]])
        allTriangles.append(coordinates[triangles[t + 2]])
    return np.array(allTriangles, np.float32)


def format_vertices2(coordinates, triangles, squares):
    all_vertices = []
    for t in range(0, len(triangles), 3):
        all_vertices.append(coordinates[triangles[t]])
        all_vertices.append(coordinates[triangles[t + 1]])
        all_vertices.append(coordinates[triangles[t + 2]])
    for t in range(0, len(squares), 4):
        all_vertices.append(coordinates[squares[t]])
        all_vertices.append(coordinates[squares[t + 1]])
        all_vertices.append(coordinates[squares[t + 2]])
        all_vertices.append(coordinates[squares[t + 3]])
    return np.array(all_vertices, np.float32)


def format_vertices3(coordinates, faces):
    all_vertices = []
    if len(faces) % 3 == 0:
        for t in range(0, len(faces), 3):
            all_vertices.append(coordinates[faces[t]])
            all_vertices.append(coordinates[faces[t + 1]])
            all_vertices.append(coordinates[faces[t + 2]])
    elif len(faces) % 4 == 0:
        for t in range(0, len(faces), 4):
            all_vertices.append(coordinates[faces[t]])
            #if(coordinates[faces[t + 1]):
            all_vertices.append(coordinates[faces[t + 1]])
            all_vertices.append(coordinates[faces[t + 2]])
            all_vertices.append(coordinates[faces[t + 3]])
    return np.array(all_vertices, np.float32)


def compile_shader(shader_type, shader_source):
    shader_id = glCreateShader(shader_type)
    glShaderSource(shader_id, shader_source)
    glCompileShader(shader_id)
    compile_success = glGetShaderiv(shader_id, GL_COMPILE_STATUS)
    if not compile_success:
        error_message = glGetShaderInfoLog(shader_id)
        glDeleteShader(shader_id)
        error_message = "\n" + error_message.decode("utf-8")
        raise Exception(error_message)
    return shader_id


def create_program(vertex_shader_code, fragment_shader_code):
    vertex_shader_id = compile_shader(GL_VERTEX_SHADER, vertex_shader_code)
    fragment_shader_id = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_code)
    program_id = glCreateProgram()
    glAttachShader(program_id, vertex_shader_id)
    glAttachShader(program_id, fragment_shader_id)
    glLinkProgram(program_id)
    link_success = glGetProgramiv(program_id, GL_LINK_STATUS)
    if not link_success:
        info = glGetProgramInfoLog(program_id)
        raise RuntimeError(info)
    glDeleteShader(vertex_shader_id)
    glDeleteShader(fragment_shader_id)
    return program_id
