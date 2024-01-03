import tkinter as tk
from game_module import Game

#bagian utama dari program 
if __name__ == "__main__":
    #tentukan path untuk gambar latar belakang 
    bg_image_path = r"C:\Airplane_Project\background_Game.jpg"
    
    #buat jendela utama Tkinter dan instance(objek yang dibuat berdasarkan class)game
    root = tk.Tk()
    game = Game(root, bg_image_path)
    
    #mulai loop utama Tkinter
    root.mainloop()
