"""
Core Game Engine and Save/Load System for Escape the Legacy Monolith.
"""

import json
import os
import sys
import time
from .player import Player
from .ui import Colors, print_banner, select_choice, type_text
from .story import scene_intro, chapter_1_gateway, chapter_2_labyrinth, chapter_3_boss, epilogue

SAVE_FILE = os.path.join(os.path.dirname(__file__), "..", "savegame.json")

class GameEngine:
    def __init__(self):
        self.player: Player = None

    def save_game(self) -> bool:
        if not self.player:
            return False
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.player.to_dict(), f, indent=2)
            print(f"\n{Colors.GREEN}💾 Game progress successfully saved to savegame.json!{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}Save failed: {e}{Colors.RESET}")
            return False

    def load_game(self) -> bool:
        if not os.path.exists(SAVE_FILE):
            print(f"{Colors.YELLOW}No savegame.json found! Start a new adventure first.{Colors.RESET}")
            return False
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.player = Player.from_dict(data)
            print(f"\n{Colors.GREEN}📂 Welcome back, {self.player.name}! Level {self.player.level} restored.{Colors.RESET}")
            return True
        except Exception as e:
            print(f"{Colors.RED}Load failed: {e}{Colors.RESET}")
            return False

    def start_new_game(self):
        print_banner()
        name = input(f"{Colors.CYAN}Enter your Developer Hacker Handle [DevHacker]: {Colors.RESET}").strip()
        if not name:
            name = "DevHacker"
        self.player = Player(name=name)
        print(f"\n{Colors.GREEN}Character initialized: {self.player.name} ready for Hacktoberfest 2026!{Colors.RESET}")
        time.sleep(0.5)

    def run_campaign(self):
        if not self.player:
            self.start_new_game()

        scene_intro(self.player)

        # Chapter 1
        if not chapter_1_gateway(self.player):
            self.game_over()
            return
        self.prompt_checkpoint("Chapter 1: The Gateway")

        # Chapter 2
        if not chapter_2_labyrinth(self.player):
            self.game_over()
            return
        self.prompt_checkpoint("Chapter 2: The Labyrinth")

        # Chapter 3
        if not chapter_3_boss(self.player):
            self.game_over()
            return

        # Epilogue
        epilogue(self.player)
        print(f"\n{Colors.CYAN}{Colors.BOLD}🎉 Congratulations on conquering Escape the Legacy Monolith!{Colors.RESET}\n")

    def prompt_checkpoint(self, checkpoint_name: str):
        print(f"\n{Colors.CYAN}📍 Checkpoint reached: {checkpoint_name}{Colors.RESET}")
        choice = select_choice("Checkpoint Options:", [
            "Continue immediately to next chamber",
            "Save game progress and continue",
            "Save and exit to desktop"
        ])
        if choice == 2:
            self.save_game()
        elif choice == 3:
            self.save_game()
            print("Thanks for playing! See you on the next commit.")
            sys.exit(0)

    def game_over(self):
        print(f"\n{Colors.RED}{Colors.BOLD}GAME OVER. Refactor failed. Better luck next sprint!{Colors.RESET}")
