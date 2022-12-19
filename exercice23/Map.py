from pyglet import sprite
from Brick import Brick


class Map:
    def __init__(self, filename, background_img:sprite, database_img:sprite):
        self.txt_map=""
        with open(filename) as map:
            self.txt_map = map.read()

        lines = self.txt_map.split("\n")
        brick_size = 2
        temp = list()
        for line in lines:
            temp.append([line[i:i+brick_size]
                    for i in range(0, len(line), brick_size)])
        self.lines = temp[:]

        brick_x = 0
        brick_y = background_img.height
        bricks = list()
        for line in self.lines:
            brick_y -= 22
            brick_x = 0
            for _brick in line:
                brick_x += 55
                if _brick != "  " and len(_brick) >= 2:
                    new_brick = Brick(database_img, _brick[0], int(_brick[1]), brick_x, brick_y)
                    bricks.append(new_brick)

        self.bricks= bricks[:]
