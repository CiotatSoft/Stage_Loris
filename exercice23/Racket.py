from BoundingBox import add_collision_box
from pyglet import sprite, image

class Racket():
    def __init__(self, _img: image, x: int, y: int):
        self.sprite = sprite.Sprite(_img.get_region(57, 512-331, 147-57, 331-302))
        self.sprite.x = x
        self.sprite.y = y
        add_collision_box(self)

