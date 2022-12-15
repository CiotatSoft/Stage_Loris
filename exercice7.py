#!/usr/bin/env python3

from pyglet import window, app, image, sprite, clock


win =  window.Window(height=768, width=1002)
logger = window.event.WindowEventLogger()
win.push_handlers(logger)


_image   = image.load("assets/images/neon_version.png")


racket = sprite.Sprite(img=_image.get_region(57, 512-331, 147-57,331-302 ))
ball = sprite.Sprite(img = _image.get_region(64,512-143, 16,16))
ball.y = 29
ball.x = racket.x + racket.width/2 - ball.width/2
ball.is_idle = True
ball.directionX=0
ball.directionY=0


def update(dt):
    if ball.x <= 0 or ball.x >=win.width-ball.width:
        ball.directionX=-ball.directionX

    if ball.y >= win.height-ball.height:
        ball.directionY=-ball.directionY

    if ball.y < racket.height:
        if ball.x > racket.x and ball.x < racket.width+racket.x:
            ball.directionY=-ball.directionY

    ball.x+=ball.directionX
    ball.y+=ball.directionY


@win.event
def on_mouse_motion(x,y,dx,dy):
    print("mouse x=%d, y=%d, dx=%d, dy=%d" % (x, y, dx, dy))
    racket.x = x
    if ball.is_idle:
        ball.x = racket.x + racket.width/2 - ball.width/2
    

@win.event
def on_mouse_press(x,y,button,modifiers):
    if window.mouse.LEFT == button:
        print("mouse.LEFT")
        ball.directionX=-4
        ball.directionY=4
        ball.is_idle= False
    elif window.mouse.RIGHT == button:
        print("mouse.RIGHT")



@win.event
def on_draw():
    win.clear()
    ball.draw()
    racket.draw()


# Call update 60 times a second
clock.schedule_interval(update, 1/60.)
app.run()



