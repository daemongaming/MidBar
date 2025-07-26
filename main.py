# VRChat Midnight Bar text-based simulator

# --- IMPORTS ---
import sys, os, random, json
from datetime import datetime

# --- DATA FILES ---

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_json(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None
    
# --- MAIN FUNCTION ---

class Main():
    
    # --- INITIALIZATION ---
    
    def __init__(self):
        self.bars = load_json(os.path.join(DATA_DIR, "bars.json"))
        self.drinks = load_json(os.path.join(DATA_DIR, "drinks.json"))
        self.commands = ["order", "drink", "look"]
        self.quits = ["quit", "exit", "leave", "bye", "goodbye", "gtfo"]
        self.drinks_on_bar = []
        # Startup welcome text
        self.bar_names = list(self.bars.keys())
        self.bars_open = []
        self.drink_ids = list(self.drinks.keys())
        print("\nWelcome to...\n\n======================\nMIDNIGHTS IN VA11 HALL-A!\n======================")
        print(f"\nBars currently open: ")
        self.bars_count = 0
        bars_open_count = 0
        for bar in self.bar_names:
            self.bars_count += 1
            days = self.bars.get(bar).get("days")
            hours = self.bars.get(bar).get("hours")
            days_of_week = {
                "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
                "Friday": 4, "Saturday": 5, "Sunday": 6
            }
            current_week_day = datetime.now().strftime("%A")
            today_index = days_of_week.get(current_week_day)
            current_hour = datetime.now().hour
            bar_open = days[today_index] and current_hour in range(hours[0], hours[1])
            if bar_open:
                bars_open_count += 1
                self.bars_open.append(bar)
                print(f"  {bars_open_count}.) {bar}")
        print("\nWhat bar would you like to visit?\n\nEnter bar name: ")
        self.bar_choice = input().strip()
        self.playing = True
        self.choosing_bar = True
        while self.choosing_bar:
            if self.bar_choice in self.bars_open:
                print(f"You walk across light puddles of rain water as you enter \"{self.bar_choice}\".\n\nFinding an empty seat at the bar, you wave down the bartender for a drink.")
                opener = self.bars.get(self.bar_choice).get("opener")
                print(f"\nThe bartender looks you up and down, before coming over and saying, \"{opener}\"")
                self.choosing_bar = False
            else:
                print(f"\nNo bar named \"{self.bar_choice}\" could be found! :( Please try again.\n\nEnter bar name: ")
                self.bar_choice = input().strip()
        # Game loop (play)
        while self.playing:
            cmd = input().strip()
            command_parts = cmd.split(" ")
            cmd_part_1 = command_parts[0].lower()
            if cmd_part_1 in self.commands:
                self.do_command(cmd)
            elif cmd_part_1 in self.quits:
                self.playing = False
            else:
                print("\n\"Sorry, what's that...?\"")

    # --- GAME COMMANDS ---
    
    def do_command(self, cmd):
        command_parts = cmd.split(" ")
        cmd_part_1 = command_parts[0].lower()
        ids = self.get_drinks_ids()
        if len(command_parts) > 1:
            drink_name = command_parts[1].lower()
            if len(command_parts) > 2:
                drink_id_count = 0
                for part in command_parts:
                    if drink_id_count > 1:
                        drink_name = drink_name + " " + part.lower()
                    drink_id_count += 1
            if cmd_part_1 == "order":
                if drink_name in ids:
                    self.serve(drink_name)
                else:
                    print(f"\n\"Sorry, I don't recognize '{drink_name}'...\"")
            elif cmd_part_1 == "drink":
                if drink_name in ids:
                    self.drink(drink_name)
                else:
                    print(f"\n\"Sorry, I don't recognize '{drink_name}'...\"")
            else:
                if cmd in ids:
                    self.drink(drink_name)
                else:
                    print(f"\n\"Sorry, I don't recognize '{drink_name}'...\"")
        elif cmd_part_1 in self.quits:
            self.playing = False
        else:
            if cmd_part_1 in ids:
                self.drink(drink_name)
            elif cmd_part_1 == "look":
                print(f"\nDrinks currently served on the bar: \n")
                drink_bar_count = 0
                for drink_on_bar in self.drinks_on_bar:
                    drink_bar_count += 1
                    print(f"  {drink_bar_count}.) {drink_on_bar}")

    # --- UTILITY FUNCTIONS ---

    def get_drinks_ids(self):
        drink_names = []
        for key in self.drink_ids:
            drink_names.append(key.lower())
        return drink_names

    def serve(self, drink_name):
        drink_upper = drink_name.upper()
        self.drinks_on_bar.append(drink_upper)
        print(f"\n\"There ya go -- enjoy your {drink_upper}, and remember to tip your bartender! ;)\"")
        
    def drink(self, drink_name):
        drink_upper = drink_name.upper()
        if drink_upper in self.drinks_on_bar:
            self.drinks_on_bar.remove(drink_upper)
            print(f"\nYou drink the {drink_upper}, and you feel drunker!")
        else:
            print(f"\nThere is no {drink_upper} served!")
    
# --- CALL TO MAIN & START GAME! ---
Main()