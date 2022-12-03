from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mouse_sensitivity = (155, 155)

class PlayerRepresentation(Entity):
    def __init__(self, position = (5,5,5)):
        super().__init__(
            parent = scene,
            position = position,
            model = "zombie.obj",
            texture = "skin.png",
            origin_y = .5,
            color = color.white,
            highlight_color = color.white,
            scale = (0.1, 0.1, 0.1)
        )
        print("HELLO !")