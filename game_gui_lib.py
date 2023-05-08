from __future__ import annotations

from time import time_ns

from imagehelper import *
from spritelib import *


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

	# def get_position(self,sprite: Sprite):
	# 	return print(self.canvas.coords(sprite.x))


class FallingObjectGameFrame(AnimatedGameFrame):
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
	
		self.bg_sprite = Sprite(0,0,canvas_width,canvas_height,image=self.bg_image)
		self.bg_sprite.draw(self.canvas)
		self.hero = AnimatedHorizontalMovingSprite(self.player_images['Left'],self.player_images['Right'],
												   self.canvas_width//2,self.canvas_height - 50,border_width=0)
		self.hero.draw(self.canvas)
		self.coins = AnimatedRandomFallingObjects(self.coin_images,bottom_limit=750)
		
		self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
								font=("Comic Sans MS", self.start_game_message_font_size),
								text=self.start_game_message, fill='white')
		
		
		self.drawables = [self.bg_sprite,self.hero, self.coins]
		self.updateables = [self.hero, self.coins]
		
		
		
		
		
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
		self.player_images = dict({
			'Left': self.images[4:8],
			'Right': self.images[8:12],
			'Up': self.images[12:16],
			'Down': self.images[0:4]})
		self.coin_images = ImageHelper.slice_to_list("images/electric_ball_sheet.png", 9, 1, 35, 35)
		self.bg_image = ImageHelper.get_sized_image('images/moon_bg.jpg',self.canvas_width,self.canvas_height)
		
	def quit(self,evt=None):
		self.root.quit()
		
	def reset_game(self,evt=None):
		print('reset')
		self.load_assets()
		
		self.lives = 3
		self.points = 0
		self.gameover = False
		self.stop()
		
		self.bg_sprite.draw(self.canvas)
		
		self.hero.sprite.center_x = self.canvas_width//2

		self.hero.draw(self.canvas)
		for coin in self.coins.objects:
			coin.reset_position()
		
		self.canvas.create_text(self.canvas_width // 2, self.canvas_height // 2,
								font=("Comic Sans MS", self.start_game_message_font_size),
								text=f'Press Left/Right\nArrows to Begin', fill='white')
	
	def speed_up(self,evt):
		
		self.hero.mover.speed += 2
		print(self.hero.mover.speed)
		if self.hero.mover.delay_time > self.delay_time:
			self.hero.mover.delay_time -= 5
		
	def reduce_speed(self,evt):
		if self.hero.mover.speed > 2:
			self.hero.mover.speed -= 2
		self.hero.mover.delay_time += 5
		
	def toggle_play(self,evt):
		if self.is_paused:
			self.start()
		else:
			self.stop()
		
	def direction_handler(self, evt):
		if self.is_paused and not self.gameover:
			self.start()
		if evt.keysym == 'Left':
			self.hero.mover.direction = Direction.LEFT
		elif evt.keysym == 'Right':
			self.hero.mover.direction = Direction.RIGHT
		elif evt.keysym == 'Up':
			self.hero.mover.direction = Direction.UP
		elif evt.keysym == 'Down':
			self.hero.mover.direction = Direction.DOWN
	
	def update(self):
		super().update()
				
		intersections = self.coins.intersects(self.hero.sprite.bbox())
		self.points += len(intersections)
		#self.get_position(self.hero.sprite)
		for obj in intersections:
			obj.reset_position()
		for coin in self.coins.objects:
			if coin.sprite.top > self.canvas_height:
				self.lives -= 1
				coin.reset_position()
				if self.lives <= 0:
					self.gameover = True
					self.lives = 0
					
					
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