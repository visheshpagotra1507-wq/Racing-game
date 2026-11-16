import random
import time
import sys

# --- GAME DATA ---
CARS = {
    "1": {"name": "Starter Hatchback", "price": 0, "speed": 10, "handling": 8},
    "2": {"name": "Porsche 911 GT3", "price": 500, "speed": 18, "handling": 15},
    "3": {"name": "Ferrari SF90", "price": 1200, "speed": 22, "handling": 14},
    "4": {"name": "Bugatti Chiron", "price": 2500, "speed": 26, "handling": 12},
}

MODES = {
    "1": "Classic Circuit (Race against aggressive AI)",
    "2": "Time Attack (Beat the clock before it runs out)",
    "3": "Elimination (Last place gets blown up every 10 seconds)"
}

UNEXPECTED_EVENTS = [
    {"name": "An angry flock of geese blocks the track!", "effect": -5, "type": "bad"},
    {"name": "Sudden localized EMP storm!", "effect": -8, "type": "bad"},
    {"name": "A secret nitrous slipstream opens up!", "effect": 10, "type": "good"},
    {"name": "A rival drops a massive banana peel!", "effect": -4, "type": "bad"},
    {"name": "Tailwind boost from a passing helicopter!", "effect": 6, "type": "good"}
]

# --- PLAYER PROFILE ---
class Player:
    def __init__(self):
        self.coins = 100
        self.unlocked_cars = ["1"]
        self.current_car = "1"
        self.score = 0

    def get_car_name(self):
        return CARS[self.current_car]["name"]

    def get_car_stat(self, stat):
        return CARS[self.current_car][stat]

# --- GAME ENGINE ---
class RacingGame:
    def __init__(self):
        self.player = Player()

    def run(self):
        print("  WELCOME TO HYPERDRIVE: OFF-LINE RACING ")
        while True:
            print("\n--- MAIN MENU ---")
            print(f"Current Car: {self.player.get_car_name()} | Coins: {self.player.coins} | High Score: 🏆 {self.player.score}")
            print("1. Enter Race")
            print("2. Visit Luxury Car Dealership")
            print("3. Exit Game")
            
            choice = input("Select an option: ").strip()
            if choice == "1":
                self.start_race_sequence()
            elif choice == "2":
                self.car_shop()
            elif choice == "3":
                print("Thanks for playing! Keeping the rubber burning.")
                break
            else:
                print("Invalid input. Try again.")

    # --- SECURITY/LOADING CAPTCHA ---
    def loading_security_check(self):
        print("\n[LOADING ASSETS & VERIFYING ANTI-CHEAT]...")
        time.sleep(1)
        
        # Driving-themed security codes
        safety_codes = ["BUCKLE_UP", "DRIFT_KING", "NO_LIMIT", "BRAKE_LATE", "TURBO_CHARGE"]
        secure_code = random.choice(safety_codes)
        
        print("\n SECURITY CAPTCHA REQUIRED TO IGNITE ENGINE ")
        print(f"Type the following driving authorization code exactly: [ {secure_code} ]")
        
        start_time = time.time()
        user_input = input("Enter Code: ").strip()
        end_time = time.time()

        if user_input == secure_code and (end_time - start_time) < 10:
            print(" Authentication successful. Engine Primed. Launching race...")
            time.sleep(1)
            return True
        else:
            print("Authentication failed or timed out! The pit crew locked the garage.")
            return False

    # --- CAR SHOP ---
    def car_shop(self):
        print("\n --- LUXURY CAR DEALERSHIP --- ")
        for key, car in CARS.items():
            status = "[OWNED]" if key in self.player.unlocked_cars else f"Price: {car['price']} coins"
            print(f"{key}. {car['name']} - Speed: {car['speed']}, Handling: {car['handling']} | {status}")
        
        choice = input("\nSelect a car to buy/equip (or press Enter to return): ").strip()
        if choice in CARS:
            if choice in self.player.unlocked_cars:
                self.player.current_car = choice
                print(f"Successfully equipped {CARS[choice]['name']}!")
            else:
                if self.player.coins >= CARS[choice]["price"]:
                    self.player.coins -= CARS[choice]["price"]
                    self.player.unlocked_cars.append(choice)
                    self.player.current_car = choice
                    print(f" Congratulations! You bought and equipped the {CARS[choice]['name']}!")
                else:
                    print(" Insufficient funds! Win more races to earn coins.")

    # --- RACE MODE SYSTEM ---
    def start_race_sequence(self):
        print("\n--- SELECT GAME MODE --- ")
        for key, description in MODES.items():
            print(f"{key}. {description}")
        
        mode_choice = input("Choose your mode: ").strip()
        if mode_choice not in MODES:
            print("Invalid mode. Returning to menu.")
            return

        # Trigger the unexpected loading security feature
        if not self.loading_security_check():
            return

        self.execute_race(MODES[mode_choice])

    # --- MAIN CORE RACING LOOP ---
    def execute_race(self, mode_name):
        print(f"\nGREEN LIGHT! Mode: {mode_name}")
        print(f"Driving: {self.player.get_car_name()}")
        
        distance_covered = 0
        race_length = 100
        powers = {"1": "Nitro Boost", "2": "Shield Generator"}
        used_shield = False
        
        while distance_covered < race_length:
            print(f"\nDistance Covered: [{ '▪' * (distance_covered // 10) }{ ' ' * (10 - (distance_covered // 10)) }] {distance_covered}/{race_length}m")
            print("Powers available: [1] Nitro Boost  [2] Shield Generator  [3] Hold Steady")
            
            action = input("Trigger a power or hold steady: ").strip()
            
            # Handling Powers
            speed_modifier = self.player.get_car_stat("speed")
            if action == "1":
                print("NITRO ENGAGED! Extra speed injection!")
                speed_modifier += 10
            elif action == "2":
                print("  SHIELD ACTIVATED! Protected against the next disaster.")
                used_shield = True
            
            # Base driving calculation
            distance_covered += random.randint(5, speed_modifier)

            # UNEXPECTED EVENT TRIGGER (25% chance per turn)
            if random.random() < 0.25 and distance_covered < race_length:
                event = random.choice(UNEXPECTED_EVENTS)
                print(f"\n UNEXPECTED EVENT: {event['name']}")
                
                if event["type"] == "bad":
                    if used_shield:
                        print(" Your shield absorbed the impact! No penalty!")
                        used_shield = False
                    else:
                        print(f"Ouch! Speed penalized by {event['effect']} points.")
                        distance_covered = max(0, distance_covered + event['effect'])
                else:
                    print(f"Awesome! Speed boosted by {event['effect']} points.")
                    distance_covered += event["effect"]

            time.sleep(1.5)

        # Race Completion & Scoring Rank
        print(f"\nCHEQUERED FLAG! You crossed the finish line!")
        final_rank = random.choice(["1st", "2nd", "3rd", "4th"])
        
        coin_rewards = {"1st": 500, "2nd": 300, "3rd": 150, "4th": 50}
        score_rewards = {"1st": 2000, "2nd": 1200, "3rd": 800, "4th": 200}
        
        earned_coins = coin_rewards[final_rank]
        earned_score = score_rewards[final_rank]
        
        self.player.coins += earned_coins
        self.player.score += earned_score
        
        print(f" Finish Rank: {final_rank} Place!")
        print(f" Gained: {earned_coins} coins")
        print(f" Score Gained: {earned_score} points")

# --- START GAME ---
if __name__ == "__main__":
    game = RacingGame()
    game.run()
