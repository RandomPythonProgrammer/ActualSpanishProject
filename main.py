import multiprocessing
import random
import time

import pyglet
import threading


class Application(pyglet.window.Window):
    def __init__(self, width, height):
        super(Application, self).__init__(width, height, style=pyglet.window.Window.WINDOW_STYLE_OVERLAY)
        self.width = width
        self.height = height
        frames = [
            pyglet.image.load('resources/sprite0.png'),
            pyglet.image.load('resources/sprite1.png'),
            pyglet.image.load('resources/sprite2.png'),
            pyglet.image.load('resources/sprite3.png'),
            pyglet.image.load('resources/sprite2.png'),
            pyglet.image.load('resources/sprite1.png')
        ]

        self.dialog = [
            pyglet.media.load('resources/audio0.wav'),
            pyglet.media.load('resources/audio1.wav'),
            pyglet.media.load('resources/audio2.wav'),
            pyglet.media.load('resources/audio3.wav'),
            pyglet.media.load('resources/audio4.wav'),
            pyglet.media.load('resources/audio5.wav'),
            pyglet.media.load('resources/audio6.wav'),
            pyglet.media.load('resources/audio7.wav')
        ]

        animation = pyglet.image.Animation.from_image_sequence(frames, duration=0.075, loop=True)
        self.sprite = pyglet.sprite.Sprite(animation)
        self.sprite.scale_x = width/animation.get_max_width()
        self.sprite.scale_y = height/animation.get_max_height()

        self.last_move = 0
        self.last_speak = 0
        self.move()

    def render(self, dt):
        self.clear()
        self.sprite.draw()

    def update(self, dt):
        if self.last_move > 5:
            if random.random() > 0.25:
                self.move()
            self.last_move = 0
        self.last_move += dt
        if self.last_speak > 7.5:
            if random.random() > 0.15:
                self.speak()
            self.last_speak = 0
        self.last_speak += dt

    def speak(self):
        random.choice(self.dialog).play()

    def move(self):
        threading.Thread(target=self._move).start()

    def _move(self):
        fade_time = 0.5
        start_time = time.time()
        while time.time() - start_time < fade_time:
            self.sprite.opacity = (1 - (time.time() - start_time)) * (1/fade_time) * 255
        self.sprite.opacity = 0
        self.set_location(random.randint(0, 1280), random.randint(0, 720))
        start_time = time.time()
        while time.time() - start_time < fade_time:
            self.sprite.opacity = (time.time() - start_time) * (1/fade_time) * 255

    def on_close(self):
        spawn_process(2)


def run():
    app = Application(200, 200)
    pyglet.clock.schedule(app.render)
    pyglet.clock.schedule(app.update)
    pyglet.app.run()


def spawn_process(number=1):
    for i in range(number):
        multiprocessing.Process(target=run).start()


if __name__ == '__main__':
    spawn_process()
    time.sleep(2)
    spawn_process()
