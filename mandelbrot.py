#A mandelbrot set visualizer using openGL

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
import numpy as np
import pyrr
import sys

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
void main()
{
    gl_Position =  vec4(a_position, 1.0);
}
"""

fragment_src = """
# version 330
out vec4 out_color;
uniform vec2 mouse_position;
uniform float version;
uniform float colorMode;
uniform float maxIterations;
uniform vec2 zoomCenter;
uniform float zoomFactor;

vec2 cmpxcjg(in vec2 c) {
	return vec2(c.x, -c.y);
}

vec2 cmpxmul(in vec2 a, in vec2 b) {
	return vec2(a.x * b.x - a.y * b.y, a.y * b.x + a.x * b.y);
}

vec2 cmpxpow(in vec2 c, int p) {
	for (int i = 0; i < p; ++i) {
		c = cmpxmul(c, c);
	}
    return c;
}

vec2 cmpxdiv(in vec2 a, in vec2 b) {
    return cmpxmul(a, cmpxcjg(b));
}

float cmpxmag(in vec2 c) {
    return sqrt(c.x * c.x + c.y * c.y);
}

vec2 translate(in vec2 c){
    vec2 temp = (c - 500)/250;
    return (temp * zoomFactor) + (zoomCenter-500)/250;
}

vec2 iterate(in vec2 c, in vec2 before){
    return (cmpxmul(before,before) + c);
}

void main()
{
    vec2 c = vec2(gl_FragCoord.x,gl_FragCoord.y);
    vec2 current = vec2(0,0);
    if(version == 1)
    {
        c = translate(mouse_position);
        current = translate(vec2(gl_FragCoord.x,gl_FragCoord.y));
    }
    else if(version == 2)
    {
        c = translate(c);
    }

    int iterations = 0;
    float gradient[51] = float[51](20,65,146,
                                            15,91,140,
                                            8,127,132,
                                            8,148,95,
                                            9,172,20,
                                            94,195,10,
                                            142,205,11,
                                            216,219,12,
                                            220,195,12,
                                            220,169,12,
                                            220,114,12,
                                            216,12,22,
                                            187,10,85,
                                            149,8,137,
                                            83,19,148,
                                            59,24,150,
                                            30,33,152);

    while(iterations <= maxIterations){
        current = iterate(c,current);
        if(cmpxmag(current) >= 2){
            break;
        }
        iterations += 1;
    }

    if(iterations < maxIterations){
        if (colorMode == 1)
        {
            int modulo = int(mod(iterations,17));
            out_color = vec4(gradient[modulo*3]/255,gradient[modulo*3+1]/255,gradient[modulo*3+2]/255,1.0);
        }
        else if(colorMode == 2)
        {
            float amount = (1/maxIterations)*iterations;
            out_color = vec4(amount,0.0,0.3,1.0);
        }
        else
        {
            out_color = vec4(0.0,0.0,0.2,1.0);
        }
    }
    else
    {
        out_color = vec4(0.0,0.0,0.0,1.0);
    }
}
"""

vertices = [-1,1,1,1,1,-1,-1,-1]

indices = [0,  1,  2,  3]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

def main():
    pygame.init()
    pygame.display.set_mode((1000, 1000), pygame.OPENGL|pygame.DOUBLEBUF|pygame.RESIZABLE)

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    # Vertex Buffer Object
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, vertices.itemsize * 2, ctypes.c_void_p(0))

    glUseProgram(shader)
    glClearColor(0, 0.0, 0.0, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    mouse_position_uniform_location = glGetUniformLocation(shader, "mouse_position")
    version_uniform_location = glGetUniformLocation(shader, "version")
    zoom_center_uniform_location = glGetUniformLocation(shader,'zoomCenter')
    zoom_factor_uniform_location = glGetUniformLocation(shader,'zoomFactor')
    color_mode_uniform_location = glGetUniformLocation(shader,'colorMode')
    max_iterations_uniform_location = glGetUniformLocation(shader,'maxIterations')

    running = True

    zoomFactor = 1
    zoomCenterX = zoomCenterY = 500

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoomFactor = zoomFactor * 0.90
                elif event.button == 5:
                    zoomFactor = zoomFactor * 1.1


        if pygame.mouse.get_pressed() == (1,0,0):
            (dx,dy) = pygame.mouse.get_rel()
            (dx,dy) = (dx * zoomFactor, dy* zoomFactor)
            zoomCenterX -= dx
            zoomCenterY += dy
        elif pygame.mouse.get_pressed() == (0,0,0):
            pygame.mouse.get_rel()

        (x,y) = pygame.mouse.get_pos()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniform2f(mouse_position_uniform_location, x,y)
        glUniform1f(version_uniform_location, version)
        glUniform1f(color_mode_uniform_location,colorMode)
        glUniform1f(max_iterations_uniform_location,maxIterations)
        glUniform2f(zoom_center_uniform_location, zoomCenterX, zoomCenterY)
        glUniform1f(zoom_factor_uniform_location, zoomFactor)

        glDrawArrays(GL_QUADS, 0,len(vertices))

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    failed = False

    if(len(sys.argv) < 4):
        print('Enter all arguments')
        failed = True
    else:
        if(sys.argv[1] == 'julia'):
            version = 1
        elif(sys.argv[1] == 'mandelbrot'):
            version = 2
        else:
            print('invalid first argument')
            failed = True

        if(sys.argv[2] == 'rainbow'):
            colorMode = 1
        elif(sys.argv[2] == 'flat'):
            colorMode = 2
        else:
            print('invalid second argument')
            failed = True

        try:
            maxIterations = int(sys.argv[3])
        except ValueError:
            print('invalid third argument')
            failed = True

    if (failed):
        print('Use either mandelbrot or julia as first argument')
        print('Use rainbow or flat for second argument')
        print('Enter max iterations as last argument')
    else:
        main()
