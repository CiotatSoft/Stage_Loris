from pyglet import window, app, image, sprite, clock


win = window.Window(height=768, width=1002)
logger = window.event.WindowEventLogger()
win.push_handlers(logger)


_image = image.load("assets/images/neon_version.png")
background_img = image.load("assets/images/bac_upscaled.png")


def reset_ball_position(ball):
    ball.x = racket.x + racket.width/2 - ball.width/2
    ball.y = racket.height


LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3


class bounding_box:
    def __init__(self, name: str, x1: int, y1: int, width: int, height: int):
        self.name = name
        self.x = x1
        self.y = y1
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, x={self.x}, y={self.y}, width={self.width}, height={self.height})"


def add_collision_box(sprite):
    sprite.collision_box = list()
    sprite.collision_box.append(bounding_box("left",
                                             sprite.x, sprite.y, 1, sprite.height))
    sprite.collision_box.append(bounding_box("right",
                                             sprite.x+sprite.width-1, sprite.y, 1, sprite.height))
    sprite.collision_box.append(bounding_box("up",
                                             sprite.x, sprite.y+sprite.height-1, sprite.width, 1))
    sprite.collision_box.append(bounding_box("down",
                                             sprite.x, sprite.y, sprite.width, 1))


racket = sprite.Sprite(img=_image.get_region(57, 512-331, 147-57, 331-302))
ball = sprite.Sprite(img=_image.get_region(64, 512-143, 16, 16))
back_sprite = sprite.Sprite(img=background_img.get_region(0, 0, 1002, 768))
brick_sprite = sprite.Sprite(img=_image.get_region(648, 468, 55, 22))
brick_sprite.x = win.height/2
brick_sprite.y = win.width / 2
reset_ball_position(ball)
ball.is_idle = True
ball.directionX = 0
ball.directionY = 0
add_collision_box(brick_sprite)


def is_colliding(object1, object2):
    return object1.x+object1.width >= object2.x and \
        object1.x <= object2.x + object2.width and \
        object1.y+object1.height >= object2.y and \
        object1.y <= object2.y+object2.height


def handle_collisions(ball, other_sprite):
    if ball.is_idle:
        return

    for collide_box in other_sprite.collision_box:
        if is_colliding(ball, collide_box):
            print(collide_box)
            if collide_box.name == "left" and ball.directionX > 0:
                ball.directionX = -ball.directionX

            if collide_box.name == "right" and ball.directionX < 0:
                ball.directionX = -ball.directionX

            if collide_box.name == "up" and ball.directionY < 0:
                ball.directionY = -ball.directionY

            if collide_box.name == "down" and ball.directionY > 0:
                ball.directionY = -ball.directionY
                ball.y = other_sprite.y-ball.height-1


def update(dt):
    handle_collisions(ball, brick_sprite)

    if not ball.is_idle:
        if ball.x <= 0 or ball.x >= win.width-ball.width:
            ball.directionX = -ball.directionX

        if ball.y >= win.height-ball.height:
            ball.directionY = -ball.directionY

        if ball.y < racket.height:
            if ball.x > racket.x and ball.x < racket.width+racket.x:
                ball.directionY = -ball.directionY

        ball.x += ball.directionX
        ball.y += ball.directionY


@win.event
def on_mouse_motion(x, y, dx, dy):
    print("mouse x=%d, y=%d, dx=%d, dy=%d" % (x, y, dx, dy))
    print("ball.x=%d, ball.y=%d, ball.xx=%d, ball.yy=%d" %
          (ball.x, ball.y, ball.x+ball.width, ball.y+ball.height))
    racket.x = x
    racket.y = y
    if ball.is_idle:
        ball.x = racket.x + racket.width/2 - ball.width/2
        ball.y = racket.y+racket.height


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
    ball.draw()
    racket.draw()
    brick_sprite.draw()


# Call update 240 times a second
clock.schedule_interval(update, 1/240.)
app.run()
