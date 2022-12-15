import pyglet

window = pyglet.window.Window()

from pyglet.window import mouse

@window.event
def on_mouse_motion(x, y, dx, dy):
        print(f' mouse x={x}, mouse y={y}, mouse dx={dx}, mouse dy={dy}')

pyglet.app.run()