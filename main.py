from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# Load textures
grass_texture = load_texture('assets/grass.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
block_model = 'assets/block.obj'

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model=block_model,
            origin_y=0.5,
            texture=grass_texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)
            if key == 'right mouse down':
                Voxel(position=self.position + mouse.normal)

# Flat world
for z in range(10):
    for x in range(10):
        Voxel(position=(x, 0, z))

# Player and sky
sky = Sky(texture=sky_texture)
player = FirstPersonController()
player.mouse_sensitivity = Vec2(100, 100)

# Arm
arm = Entity(
    parent=camera.ui,
    model='cube',
    texture=arm_texture,
    scale=(0.3, 0.5),
    position=(0.6, -0.6),
    rotation=(150, -10)
)

def update():
    arm.rotation_z = 35 if held_keys['left mouse'] or held_keys['right mouse'] else 0

app.run()
