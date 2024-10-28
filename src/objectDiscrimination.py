"""
Modules

"""

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg
import moderngl as mgl
import glm
import numpy as np
import pywavefront


"""
Graphics Engine

"""
# Event checker disabled (not needed)
# Updating the game is handled by the master object, which is in turn controlled by the maze GUI
class GraphicsEngine:
    
    def __init__(self, stimulusScreen):
        
        # Target objects
        self.targets = []
        self.targets.append("cheese")
        self.targets.append("cheesecake")
        
        # Initialize pygame modules
        pg.init()
        
        # Window size
        self.WIN_SIZE = (1024, 600)
        
        # Set opengl attributes
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        
        # Create opengl context
        pg.display.set_mode(self.WIN_SIZE, display = stimulusScreen, flags = pg.OPENGL | pg.DOUBLEBUF) # | pg.FULLSCREEN
        
        # Detect and use existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags = mgl.DEPTH_TEST | mgl.CULL_FACE)
        
        # Create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        
        # Scene light
        self.light = Light()
        
        # Camera
        self.camera = Camera(self)
        
        # Mesh
        self.mesh = Mesh(self)
        
        # Scene
        self.scene = Scene(self)
        
        # Renderer
        self.scene_renderer = SceneRenderer(self)
        
        # # mouse settings (DELETE LATER!!)
        # pg.event.set_grab(True)
        # pg.mouse.set_visible(True)

    def render(self):
        
        # Clear framebuffer
        self.ctx.clear( color = (1, 1, 1)) # White background. The same as walls in the maze
        
        # Render scene
        self.scene_renderer.render()
        
        # Swap buffers
        pg.display.flip()

    def get_time(self):
        
        self.time = pg.time.get_ticks() * 0.001

    # def run(self):
    #     while True:
    #         self.get_time()
    #         self.check_events()
    #         self.camera.update()
    #         self.render()
    #         self.delta_time = self.clock.tick(60) # frame rate
        
    # def check_events(self):
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
    #             self.mesh.destroy()
    #             self.scene_renderer.destroy()
    #             pg.quit()
    #             sys.exit()


"""
Camera

"""
# Some capabilities are disabled for simplicity
# They could be added later on to account for the mouse position within the maze
class Camera:
    
    def __init__(self, app, position = (0, 0, 10), yaw = -90, pitch = 0):
        
        # Camera settings
        self.FOV = 50  # deg
        self.NEAR = 0.1
        self.FAR = 100
        
        # Camera location
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        self.yaw = yaw
        self.pitch = pitch
        
        # Window
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        
        # View matrix
        self.m_view = self.get_view_matrix()
        
        # Projection matrix
        self.m_proj = self.get_projection_matrix()
        
        # # Computer mouse settings
        # self.SPEED = 0.005
        # self.SENSITIVITY = 0.04
        
    def update(self):
        
        # self.move()
        # self.rotate()
        # self.update_camera_vectors()
        
        self.m_view = self.get_view_matrix()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        return glm.perspective(glm.radians(self.FOV), self.aspect_ratio, self.NEAR, self.FAR)

    # def move(self):
    #     velocity = self.SPEED * self.app.delta_time
    #     keys = pg.key.get_pressed()
    #     if keys[pg.K_w]:
    #         self.position += self.forward * velocity
    #     if keys[pg.K_s]:
    #         self.position -= self.forward * velocity
    #     if keys[pg.K_a]:
    #         self.position -= self.right * velocity
    #     if keys[pg.K_d]:
    #         self.position += self.right * velocity
    #     if keys[pg.K_q]:
    #         self.position += self.up * velocity
    #     if keys[pg.K_e]:
    #         self.position -= self.up * velocity
    
    # def rotate(self):
        
    #     # Rotate camera
    #     rel_x, rel_y = pg.mouse.get_rel()
    #     self.yaw += rel_x * self.SENSITIVITY
    #     self.pitch -= rel_y * self.SENSITIVITY
    #     self.pitch = max(-89, min(89, self.pitch))

    # def update_camera_vectors(self):
        
    #     # Camera rotation
    #     yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

    #     # Camera location
    #     self.forward.x = glm.cos(yaw) * glm.cos(pitch)
    #     self.forward.y = glm.sin(pitch)
    #     self.forward.z = glm.sin(yaw) * glm.cos(pitch)
    #     self.forward = glm.normalize(self.forward)
    #     self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
    #     self.up = glm.normalize(glm.cross(self.right, self.forward))

    
"""
Environment Light

"""

class Light:
    
    def __init__(self, position = (-10, 10, 20), color = (1, 1, 1)):
        
        # Light settings
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(0, 0, 0)
        
        # Intensities
        self.Ia = 0.06 * self.color  # ambient
        self.Id = 0.8 * self.color  # diffuse
        self.Is = 1.0 * self.color  # specular
        
        # View matrix
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))


"""
Mesh

"""

class Mesh:
    
    def __init__(self, app):

        self.app = app
        self.vao = VAO(app.ctx, app)
        self.texture = Texture(app)

    def destroy(self):
        
        self.vao.destroy()
        self.texture.destroy()


"""
Textures

"""
# Enviorment capability disabled for simplicity
# It could be added later on for virtual reality experiments
class Texture:
    
    def __init__(self, app):
        
        # App
        self.app = app
        self.ctx = app.ctx
        
        # Load textures
        self.textures = {}
        
        if app.targets[0] == "cheese":
            self.textures['cheese'] = self.get_texture(path = 'assets/cheese/cheese.png')
            
        if app.targets[1] == "banana":
            self.textures['banana'] = self.get_texture(path = 'assets/banana/banana.png')
        elif app.targets[1] == "cheesecake":
            self.textures['cheesecake'] = self.get_texture(path = 'assets/cheesecake/cheesecake.png')
        
        self.textures['depth_texture'] = self.get_depth_texture()
        
        # self.textures['skybox'] = self.get_texture_cube(dir_path='assets/skybox/', ext='png')

    def get_texture(self, path):
        
        # Load texture
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x = False, flip_y = True)
        texture = self.ctx.texture(size = texture.get_size(), components = 3, data = pg.image.tostring(texture, 'RGB'))
        
        # Mipmaps
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        
        # Anisotropic filtering
        texture.anisotropy = 32.0
        
        return texture

    def get_depth_texture(self):
        
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    # def get_texture_cube(self, dir_path, ext='png'):
        
    #     # Load all faces of the 'cube' environment
    #     faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
    #     textures = []
    #     for face in faces:
    #         texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
    #         texture = pg.transform.scale(texture, (2048, 2048))
    #         if face in ['right', 'left', 'front', 'back']:
    #             texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
    #         else:
    #             texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
    #         textures.append(texture)
    #     size = textures[0].get_size()
    #     texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)
    #     for i in range(6):
    #         texture_data = pg.image.tostring(textures[i], 'RGB')
    #         texture_cube.write(face=i, data=texture_data)
    #     return texture_cube

    def destroy(self):
        [tex.release() for tex in self.textures.values()]


"""
Shader

"""

class ShaderProgram:
    
    def __init__(self, ctx):
        self.ctx = ctx
        self.programs = {}
        self.programs['default'] = self.get_program('default')
        self.programs['shadow_map'] = self.get_program('shadow_map')
        
        # # These 2 might not be needed
        # self.programs['skybox'] = self.get_program('skybox')
        # self.programs['advanced_skybox'] = self.get_program('advanced_skybox')

    def get_program(self, shader_program_name):
        
        with open(f'assets/shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'assets/shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]
        

"""
Scene Renderer

"""

class SceneRenderer:
    
    def __init__(self, app):
        
        # Scene
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        
        # Depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        
        # Shadow
        self.depth_fbo.clear()
        self.depth_fbo.use()
        
        # Target object (shadow)
        if self.app.showVisualStimulus is True:
            self.scene.objects[0].render_shadow()

    def main_render(self):
        
        self.app.ctx.screen.use()
        
        # Target object
        if self.app.showVisualStimulus is True:
            self.scene.objects[0].render()

    def render(self):
        
        # Scene
        self.scene.update()
        
        # Shadow
        self.render_shadow()
        
        # Object(s)
        self.main_render()

    def destroy(self):
        
        self.depth_fbo.release()


"""
Vertex array objects

"""

class VAO:
    
    def __init__(self, ctx, app):
        
        self.ctx = ctx
        self.vbo = VBO(ctx, app)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        if app.targets[0] == "cheese":
            # Cheese VAO
            self.vaos['cheese'] = self.get_vao(
                program = self.program.programs['default'],
                vbo = self.vbo.vbos['cheese'])
            # Shadow Cheese VAO
            self.vaos['shadow_cheese'] = self.get_vao(
                program = self.program.programs['shadow_map'],
                vbo = self.vbo.vbos['cheese'])
            
        if app.targets[1] == "banana":
            # Banana VAO
            self.vaos['banana'] = self.get_vao(
                program = self.program.programs['default'],
                vbo = self.vbo.vbos['banana'])
            # Shadow Banana VAO
            self.vaos['shadow_banana'] = self.get_vao(
                program = self.program.programs['shadow_map'],
                vbo = self.vbo.vbos['banana'])
        elif app.targets[1] == "cheesecake":
            # Cheesecake VAO
            self.vaos['cheesecake'] = self.get_vao(
                program = self.program.programs['default'],
                vbo = self.vbo.vbos['cheesecake'])
            # Shadow Cheesecake VAO
            self.vaos['shadow_cheesecake'] = self.get_vao(
                program = self.program.programs['shadow_map'],
                vbo = self.vbo.vbos['cheesecake'])
            
        # # skybox vao
        # self.vaos['skybox'] = self.get_vao(
        #     program=self.program.programs['skybox'],
        #     vbo=self.vbo.vbos['skybox'])

        # # advanced_skybox vao
        # self.vaos['advanced_skybox'] = self.get_vao(
        #     program=self.program.programs['advanced_skybox'],
        #     vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors = True)
        return vao

    def destroy(self):
        
        self.vbo.destroy()
        self.program.destroy()
        

"""
Vertex buffer objects

"""

class VBO:
    
    def __init__(self, ctx, app):
        
        # Load objects
        self.vbos = {}
        
        if app.targets[0] == "cheese":
            self.vbos['cheese'] = CheeseVBO(ctx)
            
        if app.targets[1] == "banana":
            self.vbos['banana'] = BananaVBO(ctx)
        elif app.targets[1] == "cheesecake":
            self.vbos['cheesecake'] = CheesecakeVBO(ctx)
        
        # self.vbos['skybox'] = SkyBoxVBO(ctx)
        # self.vbos['advanced_skybox'] = AdvancedSkyBoxVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
    
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        self.vbo.release()

class BananaVBO(BaseVBO):
    
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('assets/banana/banana.obj', cache = True, parse = True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class CheeseVBO(BaseVBO):
    
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('assets/cheese/cheese.obj', cache = True, parse = True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data
    
class CheesecakeVBO(BaseVBO):
    
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront('assets/cheesecake/cheesecake.obj', cache = True, parse = True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data

# class SkyBoxVBO(BaseVBO):
    
#     def __init__(self, ctx):
#         super().__init__(ctx)
#         self.format = '3f'
#         self.attribs = ['in_position']

#     @staticmethod
#     def get_data(vertices, indices):
#         data = [vertices[ind] for triangle in indices for ind in triangle]
#         return np.array(data, dtype='f4')

#     def get_vertex_data(self):
#         vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
#                     (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

#         indices = [(0, 2, 3), (0, 1, 2),
#                    (1, 7, 2), (1, 6, 7),
#                    (6, 5, 4), (4, 7, 6),
#                    (3, 4, 5), (3, 5, 0),
#                    (3, 7, 4), (3, 2, 7),
#                    (0, 6, 1), (0, 5, 6)]
#         vertex_data = self.get_data(vertices, indices)
#         vertex_data = np.flip(vertex_data, 1).copy(order='C')
#         return vertex_data

# class AdvancedSkyBoxVBO(BaseVBO):
    
#     def __init__(self, ctx):
#         super().__init__(ctx)
#         self.format = '3f'
#         self.attribs = ['in_position']

#     def get_vertex_data(self):
#         # in clip space
#         z = 0.9999
#         vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
#         vertex_data = np.array(vertices, dtype='f4')
#         return vertex_data


"""
Object models

"""

class BaseModel:
    
    def __init__(self, app, vao_name, tex_id, pos = (0, 0, 0), rot = (0, 0, 0), scale = (1, 1, 1)):
        
        # Settings
        self.app = app
        self.pos = pos
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        
        m_model = glm.mat4()
        
        # translate
        m_model = glm.translate(m_model, self.pos)
        
        # rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        
        # scale
        m_model = glm.scale(m_model, self.scale)
        
        return m_model

    def render(self):
        
        self.update()
        self.vao.render()

class ExtendedBaseModel(BaseModel):
    
    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        
        self.texture.use(location = 0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        
        # Resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        
        # Depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location = 1)
        
        # Shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        
        # Texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        
        # MVP
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        
        # Light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)
        self.program['m_view_light'].write(self.app.light.m_view_light)


class Banana(ExtendedBaseModel):
    
    def __init__(self, app, vao_name = 'banana', tex_id = 'banana', pos = (0, 0, 0), rot = (0, 0, 0), scale = (1, 1, 1)):
        
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
    def update(self):
        
        self.m_model = self.get_model_matrix()
        super().update()
        
        
class Cheese(ExtendedBaseModel):
    
    def __init__(self, app, vao_name = 'cheese', tex_id ='cheese', pos = (0, 0, 0), rot = (0, 0, 0), scale = (1, 1, 1)):
        
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
    def update(self):
        
        self.m_model = self.get_model_matrix()
        super().update()
        
        
class Cheesecake(ExtendedBaseModel):
    
    def __init__(self, app, vao_name = 'cheesecake', tex_id = 'cheesecake', pos = (0, 0, 0), rot = (0, 0, 0), scale = (1, 1, 1)):
        
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
    def update(self):
        
        self.m_model = self.get_model_matrix()
        super().update()


# class SkyBox(BaseModel):
    
#     def __init__(self, app, vao_name='skybox', tex_id='skybox',
#                  pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
#         super().__init__(app, vao_name, tex_id, pos, rot, scale)
#         self.on_init()

#     def update(self):
#         self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

#     def on_init(self):
#         # texture
#         self.texture = self.app.mesh.texture.textures[self.tex_id]
#         self.program['u_texture_skybox'] = 0
#         self.texture.use(location=0)
#         # mvp
#         self.program['m_proj'].write(self.camera.m_proj)
#         self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


# class AdvancedSkyBox(BaseModel):
    
#     def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
#                  pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
#         super().__init__(app, vao_name, tex_id, pos, rot, scale)
#         self.on_init()

#     def update(self):
#         m_view = glm.mat4(glm.mat3(self.camera.m_view))
#         self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

#     def on_init(self):
#         # texture
#         self.texture = self.app.mesh.texture.textures[self.tex_id]
#         self.program['u_texture_skybox'] = 0
#         self.texture.use(location=0)


"""
Scene

"""

class Scene:
    
    def __init__(self, app):
        
        # Load scene
        self.app = app
        self.objects = []

    def update(self):

        if self.app.targetLocation == 0:
            self.app.leftTarget.rot.xyz = self.app.time
        elif self.app.targetLocation == 1:
            self.app.rightTarget.rot.xyz = self.app.time

"""
Object Discrimination

"""

class objectDiscrimination:
    
    def __init__(self, stimulusScreen):
        
        # Loads the game and all its perks
        self.app = GraphicsEngine(stimulusScreen)

        if self.app.targets[0] == "cheese":
            self.app.leftTarget = Cheese(self.app, pos = (0, 0, 0), scale = (4, 4, 4)) # Left target object
        if self.app.targets[1] == "banana":
            self.app.rightTarget = Banana(self.app, pos = (0, 0, 0), scale = (5, 5, 5)) # Right target object
        elif self.app.targets[1] == "cheesecake":
            self.app.rightTarget = Cheesecake(self.app, pos = (0, 0, 0), scale = (45, 45, 45)) # Right target object
        
        self.app.showVisualStimulus = False
        self.app.targetLocation = 2 # blank
        self.app.render()
        
    def startStimulus(self, **kwargs):
        
        # Start stimulus
        self.app.showVisualStimulus = kwargs['display']
        self.app.targetLocation = kwargs['target']
        if self.app.showVisualStimulus is True:
            if self.app.targetLocation == 0:
                self.app.scene.objects.append(self.app.leftTarget)
            elif self.app.targetLocation == 1:
                self.app.scene.objects.append(self.app.rightTarget)

    # Update the stimulus
    def updateStimulus(self):
        
        if self.app.showVisualStimulus is True:
            self.app.get_time()
            # self.app.camera.update()     # for future tasks (with camera position according to mouse position in the maze)
            self.app.render()
            self.app.delta_time = self.app.clock.tick(60) # frame rate
            
    def stopStimulus(self, **kwargs):
        
        self.app.showVisualStimulus = kwargs['display']
        if self.app.showVisualStimulus is False:
            if self.app.targetLocation == 0:
                self.app.scene.objects.remove(self.app.leftTarget)
                self.app.render()
            elif self.app.targetLocation == 1:
                self.app.scene.objects.remove(self.app.rightTarget)
                self.app.render()
                
    # Cleanup
    def closeWindow(self):
        
        self.app.mesh.destroy()
        self.app.scene_renderer.destroy()
        pg.quit()
        
        