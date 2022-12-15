#!/usr/bin/env python3

from pyglet import window, app, image, sprite


win =  window.Window()
logger = window.event.WindowEventLogger()
win.push_handlers(logger)


_image = image.load("assets/images/neon_version.png")
racket = sprite.Sprite(img=_image.get_region(57, 512-331, 147-57,331-302 ))

@win.event
def on_mouse_motion(x,y,dx,dy):
    print("mouse x=%d, y=%d, dx=%d, dy=%d" % (x, y, dx, dy))
    racket.x = x

@win.event
def on_mouse_press(x,y,button,modifiers):
    if window.mouse.LEFT == button:
        print("mouse.LEFT")
    elif window.mouse.RIGHT == button:
        print("mouse.RIGHT")


@win.event
def on_draw():
    win.clear()
    racket.draw()


app.run()



