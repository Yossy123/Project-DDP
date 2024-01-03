import tkinter as tk
from PIL import ImageTk, Image
import random

class Game:
    def __init__(self, root, bg_image_path):
        self.root = root
        self.root.title("Game Pesawat Tembak-Tembakan")
        
        # Tambahkan latar belakang
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.create_image(200, 200, anchor=tk.CENTER, image=self.bg_image)
        self.canvas.pack()

        # Menggunakan gambar untuk pesawat
        self.player_image = Image.open("Plane.png")
        self.player_image = self.player_image.resize((40, 40))
        self.player_image = ImageTk.PhotoImage(self.player_image)
        self.player = self.canvas.create_image(200, 380, anchor=tk.CENTER, image=self.player_image)

        self.bullets = []
        self.score = 0

        self.score_label = self.canvas.create_text(50, 20, text="Score: 0", fill="white", anchor="nw", font=("Helvetica", 14))

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot)

        self.enemy = self.canvas.create_rectangle(random.randint(50, 350), 50, random.randint(50, 350), 10, fill="red")

        self.root.after(1000, self.move_enemy)

    def move_left(self, event):
        x, y = self.canvas.coords(self.player)
        if x > 20:
            self.canvas.move(self.player, -10, 0)

    def move_right(self, event):
        x, y = self.canvas.coords(self.player)
        if x < 380:
            self.canvas.move(self.player, 10, 0)

    def shoot(self, event):
        x, y = self.canvas.coords(self.player)
        self.bullets.append(self.canvas.create_rectangle(x - 2, y - 30, x + 2, y - 10, fill="yellow"))
        self.move_bullets()

    def move_bullets(self):
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, -10)
            x1, y1, x2, y2 = self.canvas.coords(bullet)
            if y1 < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
            if self.check_collision(bullet, self.enemy):
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)
                self.reset_enemy()
                self.increase_score()

        self.root.after(50, self.move_bullets)

    def move_enemy(self):
        self.canvas.move(self.enemy, 0, 5)
        x1, y1, x2, y2 = self.canvas.coords(self.enemy)
        if y2 > 400:
            self.reset_enemy()
        if self.check_collision(self.player, self.enemy):
            self.game_over()
        self.root.after(50, self.move_enemy)

    def check_collision(self, obj1, obj2):
        coords_obj1 = self.canvas.coords(obj1)
        if coords_obj1:
            x1, y1 = coords_obj1[:2]
            x3, y3, x4, y4 = self.canvas.coords(obj2)
            return x1 < x4 and x1 + 40 > x3 and y1 < y4 and y1 + 40 > y3
        return False

    def reset_enemy(self):
        self.canvas.coords(self.enemy, random.randint(50, 350), 50, random.randint(50, 350), 10)

    def increase_score(self):
        self.score += 1
        self.canvas.itemconfig(self.score_label, text="Score: {}".format(self.score))

    def game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Helvetica", 20))
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<space>")

if __name__ == "__main__":
    # Use double backslashes or a raw string for the file path
    bg_image_path = r"C:\Airplane_Project\background_Game.jpg"
    root = tk.Tk()
    game = Game(root, bg_image_path)
    root.mainloop()
