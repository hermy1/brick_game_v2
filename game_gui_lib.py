from __future__ import annotations
from time import time_ns
from imagehelper import *
from spritelib import *
from game_lib import *


class AnimatedGameFrame(Frame):
	def __init__(
			self, master=None, delay_time: int = 8, canvas_width: int = 800, canvas_height: int = 600,
			canvas_bg: str = 'white', paused: bool = False):
		super().__init__(master)
		self.delay_time = delay_time
		self.drawables = []
		self.updateables = []
		self.current_time = time_ns() // 1_000_000
		self.delta_time = 0
		self.canvas = Canvas(self, width=canvas_width, height=canvas_height, bg=canvas_bg)
		self.canvas.pack()
		self._paused = paused
		self.canvas_width = canvas_width
		self.canvas_height = canvas_height
	
	def start(self):
		if self._paused:
			self._paused = False
			self.animate()
	
	def stop(self):
		self._paused = True
		
	
	@property
	def is_paused(self):
		return self._paused
	
	def update(self):
		last_time = self.current_time
		self.current_time = time_ns() // 1_000_000
		self.delta_time = self.current_time - last_time
		for u in self.updateables:
			u.update(self.delta_time)
	
	def draw(self):
		self.canvas.delete('all')
		for d in self.drawables:
			d.draw(self.canvas)
	
	def animate(self):
		root = self.winfo_toplevel()
		if not self._paused:
			self.update()
			self.draw()
			root.after(self.delay_time, self.animate)





class BrickGameFrame(AnimatedGameFrame):
	def __init__(self, master=None, delay_time: int = 8, canvas_width: int = 800,
				 canvas_height: int = 600, canvas_bg: str = 'white', paused: bool = False):
		super().__init__(master, delay_time, canvas_width, canvas_height, canvas_bg, paused)
		
		self.load_assets()
		self.bind_keys()
		self.start_game_message = 'Press Left/Right\nArrows to Begin'
		self.start_game_message_font_size = 28
		self.game_over_message_font_size = 52
		self.lives = 3
		self.points = 0
		self.gameover = False
		self.stop()

		#game background
		self.bg_sprite = Sprite(0,0,canvas_width,canvas_height,image=self.bg_image)
		self.bg_sprite.draw(self.canvas)

		#game objects
		self.ball = Ball(canvas_width // 2, canvas_height // 2, 10, 'white')
		self.paddle = Paddle(canvas_width // 2 - 50, canvas_height - 50, 100, 10, 'white', canvas_width)
		self.bricks = []
		for i in range(2):
			for j in range(5):
				brick = Brick(i * 80 + 10, j * 30 + 50, 70, 20, f'#{randint(0, 0xFFFFFF):06x}')
				self.bricks.append(brick)

		self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
								font=("Comic Sans MS", self.start_game_message_font_size),
								text=self.start_game_message, fill='white')

		
		#add items to canvas
		self.drawables = [self.bg_sprite,self.paddle, self.ball,*self.bricks]
		self.updateables = [self.ball]


	def bind_keys(self):
			self.root = self.winfo_toplevel()
			self.root.bind("<Left>", self.direction_handler)
			self.root.bind("<Right>", self.direction_handler)
			self.root.bind("p", self.toggle_play)
			self.root.bind('s', self.speed_up)
			self.root.bind('a', self.reduce_speed)
			self.root.bind('y', self.reset_game)
			self.root.bind('n', self.quit)
		
	def load_assets(self):
		self.images = ImageHelper.slice_to_list("images/alien.png", 4, 4, 50, 50)

		self.bg_image = ImageHelper.get_sized_image('images/moon_bg.jpg',self.canvas_width,self.canvas_height)
		
	def quit(self,evt=None):
		self.root.quit()
		
	def reset_game(self,evt=None):
		print('reset')
		self.load_assets()
		self.ball = Ball(self.canvas_width // 2, self.canvas_height // 2, 10, 'white')
		self.paddle = Paddle(self.canvas_width // 2 - 50, self.canvas_height - 50, 100, 10, 'white', self.canvas_width)
		self.bricks = []
		for i in range(10):
			for j in range(5):
				brick = Brick(i * 80 + 10, j * 30 + 50, 70, 20, f'#{randint(0, 0xFFFFFF):06x}')
				self.bricks.append(brick)
		self.drawables = [self.bg_sprite,self.paddle, self.ball,*self.bricks]
		self.updateables = [self.ball]
		self.lives = 3
		self.points = 0
		self.gameover = False
		self.stop()
		self.canvas.delete('all')
		self.bg_sprite.draw(self.canvas)


		
		self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
								font=("Comic Sans MS", self.start_game_message_font_size),
								text=f'Press Left/Right\nArrows to Begin', fill='white')
	
	def speed_up(self,evt):
		pass
		#speed up ball
		#speed up paddle

		

		
	def reduce_speed(self,evt):
		pass

	def toggle_play(self,evt):
		if self.is_paused:
			self.start()
		else:
			self.stop()
		
	def direction_handler(self, evt):
		if self.is_paused and not self.gameover:
			self.start()
		if evt.keysym == 'Left':
			self.paddle.move_left()
		elif evt.keysym == 'Right':
			self.paddle.move_right()


	def update(self):
		super().update()
		for brick in self.bricks:
			if brick.check_collision(self.ball):
				self.points += 10
				self.bricks.remove(brick)
		# Check if the ball hits the bottom edge
		if self.ball.y + self.ball.radius >= self.canvas_height:
			self.lives -= 1
			self.ball.reset()
			# self.paddle.reset()
			if self.lives == 0:
				self.gameover = True
				self.stop()
				self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
										font=("Comic Sans MS", self.game_over_message_font_size),
										text=f'Game Over', fill='white')


		#check if the ball hits the paddle
		if self.ball.check_collision(self.paddle):
			self.ball.dy *= -1
			self.ball.y = self.paddle.y - self.ball.radius


		# Check if the ball hits the left or right edge
		if self.ball.x + self.ball.radius >= self.canvas_width or self.ball.x - self.ball.radius <= 0:
			self.ball.dx *= -1
		# Check if the ball hits the top edge
		if self.ball.y - self.ball.radius <= 0:
			self.ball.dy *= -1
		#if bricks are all gone then game over
		if len(self.bricks) == 0:
			self.gameover = True
			self.stop()
			self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
									font=("Comic Sans MS", self.game_over_message_font_size),
									text=f'You Win!', fill='white')

	# Check if the ball falls off the bottom of the frame
		#check for intersection/collision
		#reduce lives when the player looses
		#reset ball position etc
					
					
	def draw(self):
		super().draw()
		self.canvas.create_text(25,10,font=("Comic Sans MS",18),text=f'Lives: {self.lives}',anchor="nw",fill='white')
		self.canvas.create_text(775, 10, font=("Comic Sans MS", 18), text=f'Points: {self.points}', anchor="ne",fill='white')
		if self.gameover:
			self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
									font=("Comic Sans MS", self.game_over_message_font_size),
									text=f'Game Over',fill='white')
			self.canvas.create_text(self.canvas_width//2, self.canvas_height//2 + 100,
									font=("Comic Sans MS",self.game_over_message_font_size//2),
									text="Play Again (y/n)?",fill='white')
			self.stop()