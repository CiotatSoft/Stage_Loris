from BoundingBox import add_collision_box
from pyglet import image, sprite


class Brick():
    def __init__(self, _img: image, color: str, life: int, x: int, y: int):
        self.sprite = sprite.Sprite(_img.get_region(648, 468, 55, 22))
        self.sprite.x = x
        self.sprite.y = y
        self.life = life
        add_collision_box(self)
