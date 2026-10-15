#!/usr/bin/env python3
"""
Escape the Legacy Monolith: A Hacktoberfest Text Adventure
Built for MLH Global Hack Week 2026 Challenge: "Use GitHub Copilot to Build a Simple Application"
Author: Aroso Emmanuel (@emarc99)
"""

import sys
import os

# Ensure src package is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui import Colors, print_banner, select_choice
from src.engine import GameEngine

def show_lore():
    print(f"\n{Colors.CYAN}{Colors.BOLD}📜 LORE & DEVELOPER GUIDE:{Colors.RESET}")
    print(
        "Welcome to 'Escape the Legacy Monolith'!\n\n"
        "1. SANITY (HP): Decreases when bugs, merge conflicts, or production outages hit you.\n"
        "   If Sanity reaches 0, you burn out and game over.\n"
        "2. COFFEE (Energy): Required to run automated unit tests and push hotfixes.\n"
        "3. GITHUB STARS: Currency rewarded for defeating bugs and discovering clean documentation.\n"
        "4. TACTICS: In battle, use 'Unit Test Barrier' to raise defense and restore sanity,\n"
        "   or 'Hotfix Overclock' to deal massive burst damage!\n"
    )
    input(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.RESET}")

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    engine = GameEngine()

    while True:
        print_banner()
        options = [
            "Start New Adventure",
            "Load Saved Game",
            "View Game Lore & Tactics Guide",
            "Exit"
        ]
        choice = select_choice("Main Menu:", options)

        if choice == 1:
            engine.start_new_game()
            engine.run_campaign()
            break
        elif choice == 2:
            if engine.load_game():
                engine.run_campaign()
                break
        elif choice == 3:
            show_lore()
        elif choice == 4:
            print("Happy Hacktoberfest! Keep your branches clean.")
            sys.exit(0)

if __name__ == "__main__":
    main()
