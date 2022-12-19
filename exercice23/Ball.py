from BoundingBox import add_collision_box
from pyglet import sprite, image


class Ball():
    def __init__(self, _img: image):
        self.sprite = sprite.Sprite(_img.get_region(64, 512-143, 16, 16))
        self.sprite.x = 0
        self.sprite.y = 0
        self.is_idle = True
        self.directionX = 0
        self.directionY = 0
