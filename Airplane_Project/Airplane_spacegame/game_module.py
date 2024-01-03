import tkinter as tk
from PIL import ImageTk, Image
import random

class Game:
    def __init__(self, root, bg_image_path):
        #fungsi inisialisasi untuk game
        self.root = root
        self.root.title("Game Pesawat Tembak-Tembakan")

        # latar belakang untuk canvas
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.create_image(200, 200, anchor=tk.CENTER, image=self.bg_image)
        self.canvas.pack()

        # gambar buat objek pesawat
        self.player_image = Image.open("Plane.png")
        self.player_image = self.player_image.resize((40, 40))
        self.player_image = ImageTk.PhotoImage(self.player_image)
        self.player = self.canvas.create_image(200, 380, anchor=tk.CENTER, image=self.player_image)

        #inisialisasi untuk score dan peluru
        self.bullets = []
        self.score = 0

        #buat label untuk menampilkan score pada kanvas 
        self.score_label = self.canvas.create_text(50, 20, text="Score: 0", fill="white", anchor="nw", font=("Helvetica", 14))

        #bind tombol untuk gerakan pemain dan menembak
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot)

        #inisialisasi musuh dan atur gerak awalnya 
        self.enemy = self.canvas.create_rectangle(random.randint(50, 350), 50, random.randint(50, 350), 30, fill="red")
        self.root.after(1000, self.move_enemy)
        
    def move_left(self, event):
        #gerakan pesawat pemain ke kiri
        x, y = self.canvas.coords(self.player)
        if x > 20:
            self.canvas.move(self.player, -10, 0)

    def move_right(self, event):
        #gerakan pesawat pemain ke kanan
        x, y = self.canvas.coords(self.player)
        if x < 380:
            self.canvas.move(self.player, 10, 0)

    def shoot(self, event):
        #tembakan peluru dari pesawat pemain
        x, y = self.canvas.coords(self.player)
        self.bullets.append(self.canvas.create_rectangle(x - 2, y - 30, x + 2, y - 10, fill="yellow"))
        self.move_bullets()

    def move_bullets(self):
        #gerakan peluru ke atas dan periksa tabrakan dengan musuh
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
        #gerakan musuh ke bawah dan periksa tabrakan dengan pemain
        self.canvas.move(self.enemy, 0, 5)
        x1, y1, x2, y2 = self.canvas.coords(self.enemy)
        if y2 > 400:
            self.reset_enemy()
        if self.check_collision(self.player, self.enemy):
            self.game_over()
        self.root.after(50, self.move_enemy)

    def check_collision(self, obj1, obj2):
        #periksa tabrakan antara 2 objek pada canvas
        coords_obj1 = self.canvas.coords(obj1)
        if coords_obj1:
            x1, y1 = coords_obj1[:2]
            x3, y3, x4, y4 = self.canvas.coords(obj2)
            return x1 < x4 and x1 + 40 > x3 and y1 < y4 and y1 + 40 > y3
        return False

    def reset_enemy(self):
        #atur ulang posisi musuh ke lokasi acak
        self.canvas.coords(self.enemy, random.randint(50, 350), 50, random.randint(50, 350), 10)

    def increase_score(self):
        #tingkatkan score pemain dan perbarui label score
        self.score += 1
        self.canvas.itemconfig(self.score_label, text="Score: {}".format(self.score))

    def game_over(self):
        #Tampilkan tekss "Game Over" dan lepaskan fungsi tombol untuk menghentikan pemain 
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Helvetica", 20))
        self.root.unbind("<Left>")
        self.root.unbind("<Right>")
        self.root.unbind("<space>")
