from random import randint

class Brick:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline='white')

    def check_collision(self, ball):
        if (ball.x + ball.radius > self.x and ball.x - ball.radius < self.x + self.width and
                ball.y + ball.radius > self.y and ball.y - ball.radius < self.y + self.height):
            # collision detected
            ball.dy *= -1  # reverse y-direction of ball
            self.x = -1000  # move brick off screen
            self.y = -1000
            return True
        return False


class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.dx = randint(-5, 5)
        self.dy = -5


    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill=self.color)

    def update(self, dt):
        self.x += self.dx
        self.y += self.dy
        # Check if the ball hits the left or right edge
        # Check if the ball hits the top edge
        # Check if the ball hits the paddle

        # Check if the ball falls off the bottom of the frame

    def reset(self):
        self.x = 300
        self.y = 300
        self.dx = randint(-5, 5)
        self.dy = -5
    def check_collision(self, paddle):
        if (self.x + self.radius > paddle.x and self.x - self.radius < paddle.x + paddle.width and
                self.y + self.radius > paddle.y and self.y - self.radius < paddle.y + paddle.height):
            # collision detected
            self.dy *= -1


class Paddle:
    def __init__(self, x, y, width, height, color, canvas_width):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.canvas_width = canvas_width
        self.ball = None

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.height, fill=self.color, outline='white')

    def move_left(self):
        self.x = max(self.x - 40, 0)

    def move_right(self):
        self.x = min(self.x + 40, self.canvas_width - self.width)






    # def reset(self):
    #     self.x = 300
    #     self.y = 300
    #     self.dx = randint(-5, 5)
    #     self.dy = -5


