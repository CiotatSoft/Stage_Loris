#!/usr/bin/env python3


from pyglet import window, app
#import pyglet

win =  window.Window()
logger = window.event.WindowEventLogger()
win.push_handlers(logger)


@win.event
def on_mouse_motion(x: int ,y: int ,dx: int ,dy: int) :
    print("mouse x=%d, y=%d, dx=%d, dy=%d" % (x, y, dx, dy))

@win.event
def on_mouse_press(x,y,button,modifiers):
    if window.mouse.LEFT == button:
        print("mouse.LEFT")
    elif window.mouse.RIGHT == button:
        print("mouse.RIGHT")


@win.event
def on_draw():
    win.clear()


app.run()



