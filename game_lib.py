from tkinter import *
class Brick:
    pass
class Ball:
    def __init__(self, canvas, x, y, radius, direction, speed, color='white'):
        self.canvas = canvas
        self.radius = radius
        self.direction = direction
        self.speed = speed
        self.x = x
        self.y = y

        # self.item = canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def get_position(self):
        return self.canvas.coords(self.item)

    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    def draw(self,canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius)

    def update(self,dt):
        coords = self.get_position()
        width = self.canvas.winfo_width()
        if coords[0] <= 0 or coords[2] >= width:
            self.direction[0] *= -1
        if coords[1] <= 0:
            self.direction[1] *= -1
        x = self.direction[0] * self.speed
        y = self.direction[1] * self.speed
        self.move(x, y)

    def collide(self, game_objects):
        coords = self.get_position()
        x = (coords[0] + coords[2]) / 2
        y = (coords[1] + coords[3]) / 2

        for game_object in game_objects:
            if isinstance(game_object, Brick):
                game_object.on_collide(self, x, y)
