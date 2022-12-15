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


def update(dt):
    if not ball.is_idle:
        ball.x+=-1
        ball.y+=1


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



