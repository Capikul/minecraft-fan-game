from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

window.borderless = False
window.title = 'mineteen'

# Load assets
grass_texture = load_texture('assets/grass.png')
arm_texture = load_texture('assets/arm texture.png')
break_sound = Audio('assets/break.wav', autoplay=False)
break_sound.volume = 2.0

# Game state
game_paused = False
blocks_invisible = False
voxels = []

# Voxel block
class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=grass_texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=1
        )
        voxels.append(self)

    def input(self, key):
        if self.hovered and not game_paused:
            if key == 'left mouse down':
                break_sound.play()
                voxels.remove(self)
                destroy(self)
            if key == 'right mouse down':
                voxel = Voxel(position=self.position + mouse.normal)
                if blocks_invisible:
                    voxel.color = color.rgb(255,255,255) - voxel.color

# World
for x in range(20):
    for z in range(20):
        voxel = Voxel(position=(x, 0, z))

# Player
player = FirstPersonController()
player.gravity = 0.5
player.cursor.visible = True
player.speed = 5
player.mouse_sensitivity = Vec2(100, 100)

# Hand
hand = Entity(
    parent=camera.ui,
    model='cube',
    texture=arm_texture,
    scale=(0.2, 0.5, 1),
    rotation=(150, -10, 0),
    position=(0.4, -0.6)
)

# Sky & light
sky = Sky()
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

# PAUSE MENU UI
pause_menu = Entity(parent=camera.ui)
resume_button = Button(text='Resume', scale=(0.2, 0.1), y=0.15, parent=pause_menu)
settings_button = Button(text='Settings', scale=(0.2, 0.1), y=0, parent=pause_menu)
exit_button = Button(text='Exit Game', scale=(0.2, 0.1), y=-0.15, parent=pause_menu)
pause_menu.enabled = False

# SETTINGS MENU UI
settings_menu = Entity(parent=camera.ui)
invisible_button = Button(text='Invisible Blocks: OFF', scale=(0.3, 0.1), y=0.2, parent=settings_menu)
volume_slider = Slider(min=0, max=3, default=break_sound.volume, step=0.1, scale=(0.6, 0.05), y=0.05, parent=settings_menu)
volume_label = Text(text=f'Volume: {break_sound.volume:.1f}', y=0.1, parent=settings_menu, origin=(0,0), scale=1.5)
sensitivity_slider = Slider(min=20, max=300, default=player.mouse_sensitivity.x, step=5, scale=(0.6, 0.05), y=-0.1, parent=settings_menu)
sensitivity_label = Text(text=f'Sensitivity: {player.mouse_sensitivity.x:.0f}', y=-0.05, parent=settings_menu, origin=(0,0), scale=1.5)
back_button = Button(text='Back', scale=(0.2, 0.1), y=-0.25, parent=settings_menu)
settings_menu.enabled = False

def input(key):
    if key == 'escape':
        toggle_pause()

def toggle_pause():
    global game_paused
    game_paused = not game_paused
    pause_menu.enabled = game_paused
    settings_menu.enabled = False
    mouse.locked = not game_paused
    player.enabled = not game_paused

def toggle_invisible():
    global blocks_invisible
    blocks_invisible = not blocks_invisible

    for voxel in voxels:
        voxel.color = color.rgb(255,255,255) - voxel.color

    invisible_button.text = 'Invisible Blocks: ON' if blocks_invisible else 'Invisible Blocks: OFF'

def open_settings():
    pause_menu.enabled = False
    settings_menu.enabled = True

def back_to_pause_menu():
    settings_menu.enabled = False
    pause_menu.enabled = True

def update():
    if not game_paused:
        if held_keys['left mouse'] or held_keys['right mouse']:
            hand.rotation = (150, -10, 0)
        else:
            hand.rotation = (150, -10, 0)

    # Live update volume and sensitivity
    break_sound.volume = volume_slider.value
    volume_label.text = f'Volume: {break_sound.volume:.1f}'

    player.mouse_sensitivity = Vec2(sensitivity_slider.value, sensitivity_slider.value)
    sensitivity_label.text = f'Sensitivity: {sensitivity_slider.value:.0f}'

# Button callbacks
resume_button.on_click = toggle_pause
settings_button.on_click = open_settings
exit_button.on_click = application.quit
invisible_button.on_click = toggle_invisible
back_button.on_click = back_to_pause_menu

app.run()
