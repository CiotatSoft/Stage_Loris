from pyglet import window, app, image, sprite, clock
from pprint import pprint


win = window.Window(height=768, width=1002)
logger = window.event.WindowEventLogger()
win.push_handlers(logger)


_image = image.load("assets/images/neon_version.png")
background_img = image.load("assets/images/bac_upscaled.png")


class bounding_box:
    def __init__(self, name: str, x1: int, y1: int, width: int, height: int, parent:sprite):
        self.name = name
        self.x = x1
        self.y = y1
        self.width = width
        self.height = height
        self.sprite=parent

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"


def add_collision_box(obj):
    obj.collision_box = list()
    osp = obj.sprite
    obj.collision_box.append(bounding_box("left",
                                             osp.x, osp.y, 1,osp.height, obj))
    obj.collision_box.append(bounding_box("right",
                                             osp.x+osp.width-1, osp.y, 1, osp.height, obj))
    obj.collision_box.append(bounding_box("up",
                                             osp.x, osp.y+osp.height-1,osp.width, 1, obj))
    obj.collision_box.append(bounding_box("down",
                                             osp.x, osp.y, osp.width, 1, obj))



class Brick():
    def __init__(self, _img: image, color: str, life:int, x: int, y: int):
        self.sprite = sprite.Sprite(_img.get_region(648, 468, 55, 22))
        self.sprite.x = x
        self.sprite.y = y
        self.life=life
        add_collision_box(self)

class Racket():
    def __init__(self, _img: image, x: int, y: int):
        self.sprite = sprite.Sprite(_image.get_region(57, 512-331, 147-57, 331-302))
        self.sprite.x = x
        self.sprite.y = y
        add_collision_box(self)


def create_map(map: str):
    """
  ('\n'
   '  J3J3J3J3J3J3  J2J2J2J2\n'
   '  J3J3J3J3J3J3  J2J2J2J2\n'
   '  J3J3J3J3J3J3  J2J2J2J2\n'
   '  ')
   """
    lines = carte.split("\n")
    size_brick = 2
    temp = list()
    for line in lines:
        temp.append([line[i:i+size_brick]
                    for i in range(0, len(line), size_brick)])
    lines = temp[:]

    """
  [[],
 ['  ', 'J3', 'J3', 'J3', 'J3', 'J3', 'J3', '  ', 'J2', 'J2', 'J2', 'J2'],
 ['  ', 'J3', 'J3', 'J3', 'J3', 'J3', 'J3', '  ', 'J2', 'J2', 'J2', 'J2'],
 ['  ', 'J3', 'J3', 'J3', 'J3', 'J3', 'J3', '  ', 'J2', 'J2', 'J2', 'J2'],
 ['  ']]
  """

    brick_x = 0
    brick_y = background_img.height
    bricks = list()
    for line in lines:
        brick_y -= 22
        brick_x = 0
        for _brick in line:
            brick_x += 55
            if _brick != "  " and len(_brick) >= 2:
                new_brick = Brick(_image, _brick[0], int(_brick[1]), brick_x, brick_y)
                print(new_brick.sprite.x)
                bricks.append(new_brick)

    return bricks

def charger_carte(filename):
    with open(filename) as txt_carte:
        return txt_carte.read()

carte = charger_carte("level_1.txt")

bricks = create_map(carte)
pprint(bricks)


def reset_ball_position(ball, racket):
    ball.x = racket.sprite.x + racket.sprite.width/2 - ball.width/2
    ball.y = racket.sprite.height


LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


#racket = sprite.Sprite(img=_image.get_region(57, 512-331, 147-57, 331-302))
racket = Racket(_image, win.width/2, 0 )
ball = sprite.Sprite(img=_image.get_region(64, 512-143, 16, 16))
back_sprite = sprite.Sprite(img=background_img.get_region(0, 0, 1002, 768))
#brick_sprite = sprite.Sprite(img=_image.get_region(648, 468, 55, 22))
#brick_sprite.x = win.height/2
#brick_sprite.y = win.width / 2
reset_ball_position(ball, racket)
ball.is_idle = True
ball.directionX = 0
ball.directionY = 0
#add_collision_box(brick_sprite)


def is_colliding(object1, object2):
    return object1.x+object1.width >= object2.x and \
        object1.x <= object2.x + object2.width and \
        object1.y+object1.height >= object2.y and \
        object1.y <= object2.y+object2.height


def handle_collisions(ball, brick:Brick, collide_box:bounding_box, count:bool):
    if ball.is_idle:
        return

    if is_colliding(ball, collide_box):
        pprint(collide_box)
        if count and brick:
            brick.life -= 1

        if collide_box.name == "left" and ball.directionX > 0:
            ball.directionX = -ball.directionX

        if collide_box.name == "right" and ball.directionX < 0:
            ball.directionX = -ball.directionX

        if collide_box.name == "up" and ball.directionY < 0:
            ball.directionY = -ball.directionY

        if collide_box.name == "down" and ball.directionY > 0:
            ball.directionY = -ball.directionY
            ball.y = collide_box.y-ball.height-1




def update(dt):
    for brick in bricks:
        if brick.life > 0:
            for collide_box in brick.collision_box:
                handle_collisions(ball, brick, collide_box, True)

    add_collision_box(racket)
    for collide_box in racket.collision_box:
        handle_collisions(ball, None, collide_box, False)

    if not ball.is_idle:
        rs = racket.sprite
        if ball.x <= 0 or ball.x >= win.width-ball.width:
            ball.directionX = -ball.directionX

        if ball.y >= win.height-ball.height:
            ball.directionY = -ball.directionY

        if ball.y < rs.height:
            if ball.x > rs.x and ball.x < rs.width+rs.x:
                ball.directionY = -ball.directionY

        ball.x += ball.directionX
        ball.y += ball.directionY


@win.event
def on_mouse_motion(x, y, dx, dy):
    print("mouse x=%d, y=%d, dx=%d, dy=%d" % (x, y, dx, dy))
    print("ball.x=%d, ball.y=%d, ball.xx=%d, ball.yy=%d" %
          (ball.x, ball.y, ball.x+ball.width, ball.y+ball.height))
    rs = racket.sprite
    rs.x = x
    rs.y = y
    if ball.is_idle:
        ball.x = rs.x + rs.width/2 - ball.width/2
        ball.y = rs.y+rs.height


@win.event
def on_mouse_press(x, y, button, modifiers):
    if window.mouse.LEFT == button:
        print("mouse.LEFT")
        ball.directionX = 1
        ball.directionY = 1
        ball.is_idle = False
    elif window.mouse.RIGHT == button:
        reset_ball_position(ball)
        ball.is_idle = True


@win.event
def on_draw():
    win.clear()
    back_sprite.draw()

    for brick in bricks:
        if brick.life > 0:
            brick.sprite.draw()

    ball.draw()
    racket.sprite.draw()
    # brick_sprite.draw()


# Call update 240 times a second
clock.schedule_interval(update, 1/60.)
app.run()
