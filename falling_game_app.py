from tkinter import *
from game_gui_lib import *
from spritelib import *




root = Tk()
game = BrickGameFrame(root)
game.pack()

game.animate()

root.mainloop()
