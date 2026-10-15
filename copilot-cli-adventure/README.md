# 🗡️ Escape the Legacy Monolith: A Hacktoberfest Text Adventure

An interactive, terminal-based "Choose Your Own Adventure" RPG built in Python with **GitHub Copilot** for the **Major League Hacking (MLH) Global Hack Week: Hacktoberfest 2026**.

**Author:** Aroso Emmanuel ([@emarc99](https://github.com/emarc99))  
**Target Challenges:**
- 🥇 **"Use GitHub Copilot to Build a Simple Application"** (Challenge 4)
- 🥈 **"Use GitHub Copilot to complete any of this week's challenges"** (Challenge 5)

---

## 📖 The Story

You are an open-source engineer entering the subterranean server farm of a Fortune 500 tech giant during Hacktoberfest. Before you looms **The Legacy Monolith**: 4.8 million lines of undocumented spaghetti code, zero unit tests, and a single deployment script named `do_not_touch.sh`.

Your mission:
Wade through the **Gateway of Global State**, navigate the **Race Condition Labyrinth**, defeat vicious software bugs in tactical turn-based combat, and confront the dreaded **Memory Leak Dragon** to refactor production into modern clean architecture!

---

## 🎮 Core Gameplay Mechanics

### 1. Developer Vitals & Resources
- **❤️ Sanity (HP):** Your mental endurance. Drops when bugs crash production or merge conflicts explode. Reaching 0 results in burnout and game over!
- **☕ Coffee (Mana/Energy):** Consumed to deploy CI unit test shields, run automated linters, and trigger critical hotfixes.
- **⭐️ GitHub Stars (Currency):** Awarded for eliminating bugs and uncovering clean documentation scrolls.
- **🗡️ Weapons & Armor:** Upgrade from a humble *Rubber Duck Debugger* to a *Strict Null Compiler Flag*, and equip a *Docker Container Isolation Vest*.

### 2. Tactical Turn-Based Debugging Combat
Encounter software abominations like the **Null Pointer Goblin**, **Race Condition Chimera**, and the **Memory Leak Dragon**:
- `[1] Git Blame Strike:` Reliable melee attack using equipped weapon.
- `[2] Unit Test Barrier:` Spends 10 Coffee to deploy automated test barriers (+5 Defense & +12 Sanity for 2 turns).
- `[3] Hotfix Overclock:` Spends 20 Coffee to push directly to production for massive critical damage.
- `[4] Use Consumables:` Drink a Triple Espresso or read a Git Wisdom Cheatsheet.
- `[5] Git Stash:` Attempt to stash changes and flee the encounter.

### 3. Branching Storyline & 3 Unique Endings
- **Ending 1 (Microservice Ascension):** Break the monolith into 42 Kubernetes microservices. High cloud bill, but 100% uptime!
- **Ending 2 (Pragmatic Modular Monolith):** Clean domain-driven architecture with 3-second build times.
- **Ending 3 (Touch Grass Legend):** Merge the final PR, shut the laptop, and head outside under the autumn trees.

---

## 🚀 Quickstart & How to Play

### Zero External Dependencies!
The game runs on standard **Python 3.10+** using native standard libraries. No `pip install` required!

```bash
# Clone the repository
git clone https://github.com/emarc99/copilot-cli-adventure.git
cd copilot-cli-adventure

# Launch the game
python main.py
```

### Running Unit Tests
A full test suite verifies player leveling, combat mechanics, and save/load serialization:
```bash
pytest -v tests/test_game.py
```
```text
tests/test_game.py::test_player_initialization PASSED      [ 14%]
tests/test_game.py::test_damage_and_healing PASSED         [ 28%]
tests/test_game.py::test_coffee_energy_usage PASSED        [ 42%]
tests/test_game.py::test_inventory_management PASSED       [ 57%]
tests/test_game.py::test_level_up_mechanics PASSED         [ 71%]
tests/test_game.py::test_save_load_serialization PASSED    [ 85%]
tests/test_game.py::test_enemy_mechanics PASSED            [100%]
7 passed in 0.11s
```

---

## 🤖 Built with GitHub Copilot

For the complete log of prompts, architectural decisions, and iterative AI pair-programming transcripts, see [`PROMPTS.md`](./PROMPTS.md).

---

## 📄 License
MIT License. Open-source contribution for MLH Global Hack Week Hacktoberfest 2026.
