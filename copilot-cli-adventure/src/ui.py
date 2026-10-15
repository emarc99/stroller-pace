"""
Terminal UI utilities with ANSI colors, progress bars, and ASCII banners.
Gracefully handles terminals with or without color support.
"""

import sys
import time

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

def print_banner():
    banner = f"""{Colors.CYAN}{Colors.BOLD}
  ██████╗ ███████╗██████╗  █████╗ ████████╗███████╗
 ██╔═══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
 ██║   ██║███████╗██████╔╝███████║   ██║   █████╗  
 ██║   ██║╚════██║██╔═══╝ ██╔══██║   ██║   ██╔══╝  
 ╚██████╔╝███████║██║     ██║  ██║   ██║   ███████╗
  ╚═════╝ ╚══════╝╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝
   THE LEGACY MONOLITH: A HACKTOBERFEST QUEST
{Colors.RESET}"""
    print(banner)

def render_bar(label: str, current: int, maximum: int, color: str, length: int = 20) -> str:
    fraction = max(0.0, min(1.0, current / maximum if maximum > 0 else 0.0))
    filled = int(fraction * length)
    empty = length - filled
    bar = f"{color}{'█' * filled}{Colors.DIM}{'░' * empty}{Colors.RESET}"
    return f"{label:8s} [{bar}] {current:>3d}/{maximum:<3d}"

def print_status_hud(player):
    sanity_color = Colors.GREEN if player.sanity > 50 else (Colors.YELLOW if player.sanity > 25 else Colors.RED)
    coffee_color = Colors.CYAN
    print("-" * 65)
    print(f" {Colors.BOLD}{player.name}{Colors.RESET} | Level {player.level} | ⭐️ Stars: {Colors.YELLOW}{player.stars}{Colors.RESET}")
    print(f" {render_bar('Sanity', player.sanity, player.max_sanity, sanity_color)}")
    print(f" {render_bar('Coffee', player.coffee, player.max_coffee, coffee_color)}")
    print(f" 🗡️ Weapon: {player.weapon} (+{player.weapon_bonus}) | 🛡️ Armor: {player.armor} (+{player.defense_bonus})")
    print("-" * 65)

def type_text(text: str, delay: float = 0.015, color: str = Colors.RESET):
    print(color, end="", flush=True)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Colors.RESET)

def select_choice(prompt: str, options: list) -> int:
    print(f"\n{Colors.BOLD}{prompt}{Colors.RESET}")
    for idx, opt in enumerate(options, 1):
        print(f"  {Colors.YELLOW}[{idx}]{Colors.RESET} {opt}")
    
    while True:
        try:
            choice = input(f"\n{Colors.CYAN}Enter your action (1-{len(options)}): {Colors.RESET}").strip()
            val = int(choice)
            if 1 <= val <= len(options):
                return val
            print(f"{Colors.RED}Please choose between 1 and {len(options)}.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting adventure...")
            sys.exit(0)
