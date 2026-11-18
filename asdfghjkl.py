import tkinter as tk
from tkinter import messagebox
import random

class PlayableRacingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyperdrive Arcade")
        
        # Game State Variables
        self.coins, self.score, self.high_score = 100, 0, 0
        self.car_tier = 1 # 1: Starter, 2: Porsche, 3: Bugatti
        self.lane = 1     # Lanes: 0 (Top), 1 (Middle), 2 (Bottom)
        self.lane_y = [50, 110, 170]
        self.obstacles = []
        self.playing = False
        self.nitro_cool = 0
        self.security_code = str(random.randint(1000, 9999)) 

        # --- UI TOP BAR (Stats & Security) ---
        self.header = tk.Label(root, text=f"Coins: 🪙{self.coins} | Score: 🏆{self.score} | Code: {self.security_code}", font=("Arial", 12, "bold"))
        self.header.pack(pady=5)
        
        self.code_entry = tk.Entry(root, justify='center', font=("Arial", 10))
        self.code_entry.insert(0, "Type Code Here")
        self.code_entry.pack()

        # --- GAME CANVAS ---
        self.canvas = tk.Canvas(root, width=600, height=240, bg="#2c3e50")
        self.canvas.pack(pady=10)
        
        # Draw Roads Lanes
        self.canvas.create_line(0, 90, 600, 90, fill="white", dash=(10, 10))
        self.canvas.create_line(0, 150, 600, 150, fill="white", dash=(10, 10))
        
        # Player Car Asset
        self.player = self.canvas.create_rectangle(40, self.lane_y[self.lane]-15, 90, self.lane_y[self.lane]+15, fill="cyan", outline="white")

        # --- CONTROLS / SHOP BOTTOM PANEL ---
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=5)
        
        self.btn_start = tk.Button(self.btn_frame, text="🟢 Start Race", bg="green", fg="white", font=("Arial", 10, "bold"), command=self.verify_and_start)
        self.btn_start.grid(row=0, column=0, padx=10)
        
        self.btn_shop = tk.Button(self.btn_frame, text="🛒 Buy Luxury Car (🪙250)", bg="gold", font=("Arial", 10, "bold"), command=self.buy_car)
        self.btn_shop.grid(row=0, column=1, padx=10)

        # Bind Keyboard Inputs
        self.root.bind("<Up>", lambda e: self.move_lane(-1))
        self.root.bind("<Down>", lambda e: self.move_lane(1))
        self.root.bind("<space>", lambda e: self.activate_nitro())

    def verify_and_start(self):
        if self.code_entry.get() != self.security_code:
            messagebox.showerror("Security Triggered", "Incorrect security key! Ignition locked.")
            return
        
        # Clean up previous race data
        for obs in self.obstacles: self.canvas.delete(obs)
        self.obstacles.clear()
        
        self.score, self.playing = 0, True
        self.code_entry.config(state=tk.DISABLED)
        self.btn_start.config(state=tk.DISABLED)
        self.game_loop()

    def move_lane(self, direction):
        if not self.playing: return
        self.lane = max(0, min(2, self.lane + direction))
        p_coords = self.canvas.coords(self.player)
        # Shift Y position smoothly to the current lane array definition
        self.canvas.coords(self.player, p_coords[0], self.lane_y[self.lane]-15, p_coords[2], self.lane_y[self.lane]+15)

    def activate_nitro(self):
        if self.playing and self.nitro_cooldown <= 0:
            self.nitro_cooldown = 50 # Lasts for roughly 50 frames
            self.canvas.itemconfig(self.player, fill="magenta")

    def buy_car(self):
        if self.coins >= 250 and self.car_tier < 3:
            self.coins -= 250
            self.car_tier += 1
            names = {2: "Porsche 911 GT3 (Red)", 3: "Bugatti Chiron (Gold)"}
            colors = {2: "red", 3: "gold"}
            self.canvas.itemconfig(self.player, fill=colors[self.car_tier])
            messagebox.showinfo("Dealership", f"Unlocked & Equipped: {names[self.car_tier]}!")
            self.update_ui()
        else:
            messagebox.showwarning("Shop", "Not enough coins or maximum car tier reached!")

    def update_ui(self):
        self.header.config(text=f"Coins: 🪙{self.coins} | Score: 🏆{self.score} | Code: {self.security_code}")

    def game_loop(self):
        if not self.playing: return

        # 1. Spawn Obstacles / Enemy Traffic
        if random.random() < 0.05:
            spawn_lane = random.choice(self.lane_y)
            obs = self.canvas.create_rectangle(610, spawn_lane-15, 650, spawn_lane+15, fill="orange", outline="black")
            self.obstacles.append(obs)

        # 2. Unexpected Modifier Events (Dynamic text alerts)
        if random.random() < 0.005:
            event = random.choice(["ROAD BLOCKS SPAWNING FASTER!", "WEATHER DELAY: SLOWDOWN!"])
            self.canvas.create_text(300, 20, text=f"⚠️ {event}", fill="yellow", font=("Arial", 12, "bold"), tags="alert")
            self.root.after(1500, lambda: self.canvas.delete("alert"))

        # 3. Process Nitro State
        speed_multiplier = 1.8 if self.nitro_cooldown > 0 else 1.0
        if self.nitro_cooldown > 0:
            self.nitro_cooldown -= 1
            if self.nitro_cooldown == 0:
                base_colors = {1: "cyan", 2: "red", 3: "gold"}
                self.canvas.itemconfig(self.player, fill=base_colors[self.car_tier])

        # 4. Movement & Collision Evaluation Loops
        p_box = self.canvas.coords(self.player)
        self.score += int(1 * self.car_tier * speed_multiplier)
        self.update_ui()

        for obs in list(self.obstacles):
            self.canvas.move(obs, -int(7 * speed_multiplier * (1 if self.car_tier==1 else 1.2)), 0)
            o_box = self.canvas.coords(obs)

            # Collision check logic
            if o_box[0] < p_box[2] and o_box[2] > p_box[0] and o_box[1] < p_box[3] and o_box[3] > p_box[1]:
                if self.nitro_cooldown > 0: # Nitro smashes through cars!
                    self.canvas.delete(obs)
                    self.obstacles.remove(obs)
                    self.coins += 20
                    continue
                else:
                    self.game_over()
                    return

            # Clear out-of-bounds obstacles to save memory
            if o_box[2] < 0:
                self.canvas.delete(obs)
                self.obstacles.remove(obs)
                self.coins += 10 * self.car_tier

        self.root.after(30, self.game_loop) # Loop engine tick rate (~33 FPS)

    def game_over(self):
        self.playing = False
        self.high_score = max(self.high_score, self.score)
        
        # Rank calculations based on score tier achieved
        rank = "ROOKIE"
        if self.score > 1500: rank = "PRO"
        if self.score > 3500: rank = "LEGEND"

        messagebox.showinfo("CRASHED!", f"Race Over!\nFinal Score: {self.score}\nRank Earned: [{rank}]\nTotal Coins: 🪙{self.coins}")
        
        # Reset Menu Configurations
        self.security_code = str(random.randint(1000, 9999))
        self.update_ui()
        self.code_entry.config(state=tk.NORMAL)
        self.code_entry.delete(0, tk.END)
        self.code_entry.insert(0, "Type New Code")
        self.btn_start.config(state=tk.NORMAL)

if __name__ == "__main__":
    window = tk.Tk()
    game = PlayableRacingGame(window)
    window.mainloop()
