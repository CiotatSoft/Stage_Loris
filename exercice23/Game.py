from pyglet import window, app, image, sprite, clock, media, resource
from Brick import Brick
from Racket import Racket
from Map import Map
from Ball import Ball
from BoundingBox import add_collision_box, Bounding_box

#music = resource.media('Video-Game-1.mp3')
#music.play()

class Game:
    def __init__(self, resolutionX: int, resolutionY: int, map_file):
        self.resolutionX = resolutionX
        self.resolutionY = resolutionY
        win = window.Window(height=resolutionY, width=resolutionX)
        self.win = win
        self.winning = False
        self.sounds = dict()

        self.logger = window.event.WindowEventLogger()
        self.win.push_handlers(self.logger)

        self.image_database = resource.image("neon_version.png")
        self.background_img = resource.image("bac_upscaled.png")

        self.map = Map("./level_0.txt", self.background_img,
                       self.image_database)
        self.racket = Racket(self.image_database, self.win.width/2, 0)
        self.back_sprite = sprite.Sprite(
            img=self.background_img.get_region(0, 0, 1002, 768))
        self.ball = Ball(self.image_database)
        self._reset_ball_position()

        @win.event
        def on_mouse_motion(x, y, dx, dy):
            rs = self.racket.sprite
            rs.x = x
            rs.y = y
            if self.ball.is_idle:
                self.ball.sprite.x = rs.x + rs.width/2 - self.ball.sprite.width/2
                self.ball.sprite.y = rs.y+rs.height

        @win.event
        def on_mouse_press(x, y, button, modifiers):
            if window.mouse.LEFT == button:
                self.ball.directionX = -1
                self.ball.directionY = 1
                self.ball.sprite.y += 10
                self.ball.is_idle = False
            elif window.mouse.RIGHT == button:
                self._reset_ball_position()
                self.ball.is_idle = True

        @win.event
        def on_draw():
            self.win.clear()
            self.back_sprite.draw()

            for brick in self.map.bricks:
                if brick.life > 0:
                    brick.sprite.draw()

            self.ball.sprite.draw()
            self.racket.sprite.draw()

        clock.schedule_interval(self._update, 1/100.)
        app.run()

    def _update(self, dt):
        one_brick_alive=False
        for brick in self.map.bricks:
            if brick.life > 0:
                one_brick_alive=True
                for collide_box in brick.collision_box:
                    self._handle_collision(brick, collide_box)
                    
        if not one_brick_alive and not self.winning:
            self._play_sound("Win.mp3")    
            self.winning=True
                 

        add_collision_box(self.racket)
        for collide_box in self.racket.collision_box:
            self._handle_collision(None, collide_box)

        if not self.ball.is_idle:
            rs = self.racket.sprite
            if self.ball.sprite.x <= 0 or self.ball.sprite.x >= self.win.width-self.ball.sprite.width:
                self.ball.directionX = -self.ball.directionX

            if self.ball.sprite.y >= self.win.height-self.ball.sprite.height:
                self.ball.directionY = -self.ball.directionY

            if self.ball.sprite.y < rs.height:
                if self.ball.sprite.x > rs.x and self.ball.sprite.x < rs.width+rs.x:
                    self.ball.directionY = -self.ball.directionY

            self.ball.sprite.x += self.ball.directionX
            self.ball.sprite.y += self.ball.directionY

    def _reset_ball_position(self):
        self.ball.sprite.x = self.racket.sprite.x + \
            self.racket.sprite.width/2 - self.ball.sprite.width/2
        self.ball.sprite.y = self.racket.sprite.y + self.racket.sprite.height

    @staticmethod
    def _is_colliding(object1, object2):
        return object1.x+object1.width >= object2.x and \
            object1.x <= object2.x + object2.width and \
            object1.y+object1.height >= object2.y and \
            object1.y <= object2.y+object2.height

    def _handle_collision(self, brick: Brick, collide_box: Bounding_box):
        if self.ball.is_idle:
            return

        if self._is_colliding(self.ball.sprite, collide_box):
        
            if brick:
                brick.life -= 1
                self._play_sound("Coin.mp3")

            if collide_box.name == "left" and self.ball.directionX > 0:
                self.ball.directionX = -self.ball.directionX

            if collide_box.name == "right" and self.ball.directionX < 0:
                self.ball.directionX = -self.ball.directionX

            if collide_box.name == "up" and self.ball.directionY < 0:
                self.ball.directionY = -self.ball.directionY

            if collide_box.name == "down" and self.ball.directionY > 0:
                self.ball.directionY = -self.ball.directionY
                self.ball.sprite.y = collide_box.y-self.ball.sprite.height-1

        

    def _play_sound(self, sound_file_name:str):
        if sound_file_name not in self.sounds:
            self.sounds[sound_file_name] = media.StaticSource(media.load(sound_file_name))
        self.sounds[sound_file_name].play()
         
        

