"""
Combat engine for debugging battles in Escape the Legacy Monolith.
"""

import random
import time
from .ui import Colors, render_bar, select_choice

class Enemy:
    def __init__(self, name: str, hp: int, attack: int, xp_reward: int, stars_reward: int, lore: str):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.xp_reward = xp_reward
        self.stars_reward = stars_reward
        self.lore = lore

    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int) -> int:
        self.hp = max(0, self.hp - amount)
        return amount

def run_battle(player, enemy: Enemy) -> bool:
    print(f"\n{Colors.RED}{Colors.BOLD}⚔️ ENCOUNTER! A wild {enemy.name} has appeared!{Colors.RESET}")
    print(f"{Colors.DIM}\"{enemy.lore}\"{Colors.RESET}\n")

    barrier_turns = 0

    while player.is_alive() and enemy.is_alive():
        # Display Combat HUD
        print("-" * 55)
        print(f" {Colors.RED}👾 {enemy.name}{Colors.RESET}")
        print(f" {render_bar('Health', enemy.hp, enemy.max_hp, Colors.RED)}")
        print(f"\n {Colors.CYAN}🧑💻 {player.name}{Colors.RESET}")
        print(f" {render_bar('Sanity', player.sanity, player.max_sanity, Colors.GREEN)}")
        print(f" {render_bar('Coffee', player.coffee, player.max_coffee, Colors.CYAN)}")
        if barrier_turns > 0:
            print(f" {Colors.BLUE}🛡️ Active Unit Test Shield ({barrier_turns} turns remaining){Colors.RESET}")
        print("-" * 55)

        options = [
            f"Git Blame Strike (Deals {10 + player.weapon_bonus} - {18 + player.weapon_bonus} dmg)",
            f"Unit Test Barrier (10 Coffee | +5 Def & +12 Sanity for 2 turns)",
            f"Hotfix Overclock (20 Coffee | Massive Strike 30-45 dmg)",
            "Drink Coffee / Use Item",
            "Git Stash (Flee encounter)"
        ]

        action = select_choice("Select your debugging tactic:", options)

        # 1. Basic Strike
        if action == 1:
            dmg = random.randint(10 + player.weapon_bonus, 18 + player.weapon_bonus)
            actual_dmg = enemy.take_damage(dmg)
            print(f"\n{Colors.GREEN}💥 You swung your {player.weapon} for {actual_dmg} refactoring damage!{Colors.RESET}")
        
        # 2. Unit Test Barrier
        elif action == 2:
            if player.use_coffee(10):
                barrier_turns = 2
                healed = player.heal(12)
                print(f"\n{Colors.BLUE}🛡️ You deployed automated CI unit tests! Restored {healed} Sanity; Defense boosted!{Colors.RESET}")
            else:
                print(f"\n{Colors.YELLOW}☕ Not enough Coffee to run tests! Take another action.{Colors.RESET}")
                continue

        # 3. Hotfix Overclock
        elif action == 3:
            if player.use_coffee(20):
                dmg = random.randint(30, 45) + player.weapon_bonus
                actual_dmg = enemy.take_damage(dmg)
                print(f"\n{Colors.MAGENTA}⚡ CRITICAL HIT! You pushed a hotfix directly to main for {actual_dmg} damage!{Colors.RESET}")
            else:
                print(f"\n{Colors.YELLOW}☕ Not enough Coffee for an overclock! Choose another action.{Colors.RESET}")
                continue

        # 4. Item Menu
        elif action == 4:
            consumables = [item for item in player.inventory if item.get("type") == "consumable"]
            if not consumables:
                print(f"\n{Colors.YELLOW}No consumables in inventory!{Colors.RESET}")
                continue
            item_opts = [f"{item['name']} (x{item['qty']})" for item in consumables]
            item_opts.append("Cancel")
            sub_choice = select_choice("Choose item to use:", item_opts)
            if sub_choice > len(consumables):
                continue
            chosen = consumables[sub_choice - 1]
            if "restore_coffee" in chosen:
                gained = player.restore_energy(chosen["restore_coffee"])
                print(f"\n{Colors.CYAN}☕ You drank {chosen['name']} and recovered {gained} Coffee!{Colors.RESET}")
            if "restore_sanity" in chosen:
                gained = player.heal(chosen["restore_sanity"])
                print(f"\n{Colors.GREEN}❤️ You read {chosen['name']} and recovered {gained} Sanity!{Colors.RESET}")
            player.remove_item(chosen["id"], 1)

        # 5. Flee
        elif action == 5:
            if random.random() > 0.4:
                print(f"\n{Colors.YELLOW}🏃 You stashed your unstaged changes and escaped safely!{Colors.RESET}")
                return True
            else:
                print(f"\n{Colors.RED}❌ Git merge conflict! You failed to escape!{Colors.RESET}")

        # Check enemy death
        if not enemy.is_alive():
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 DEFEATED! You eliminated {enemy.name}!{Colors.RESET}")
            player.stars += enemy.stars_reward
            leveled = player.add_xp(enemy.xp_reward)
            print(f"⭐️ Earned: +{enemy.stars_reward} GitHub Stars, +{enemy.xp_reward} XP!")
            if leveled:
                print(f"{Colors.YELLOW}{Colors.BOLD}🚀 LEVEL UP! You reached Level {player.level}! Max Sanity & Coffee Increased!{Colors.RESET}")
            time.sleep(1.0)
            return True

        # Enemy turn
        effective_def = player.defense_bonus + (6 if barrier_turns > 0 else 0)
        enemy_dmg = max(2, enemy.attack + random.randint(-2, 4) - effective_def)
        player.take_damage(enemy_dmg)
        print(f"{Colors.RED}💥 {enemy.name} attacked! Inflicted {enemy_dmg} damage to your Sanity!{Colors.RESET}")

        if barrier_turns > 0:
            barrier_turns -= 1

        time.sleep(0.8)

    # Defeat check
    if not player.is_alive():
        print(f"\n{Colors.RED}{Colors.BOLD}💀 YOUR SANITY REACHED 0! The Legacy Monolith crashed production...{Colors.RESET}")
        return False
    return True
