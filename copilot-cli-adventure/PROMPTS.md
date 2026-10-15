# 🤖 GitHub Copilot Pair Programming Log & Prompts

**Project:** Escape the Legacy Monolith: A Hacktoberfest Text Adventure  
**Challenge:** MLH Global Hack Week — *"Use GitHub Copilot to Build a Simple Application"* (Challenge 4)  
**Author:** Aroso Emmanuel (`@emarc99`)  
**AI Assistant:** GitHub Copilot / AI Pair Programming  

---

## 💡 Overview
This document logs the step-by-step prompts, architectural decisions, and iterative refinement workflow used while co-developing **Escape the Legacy Monolith** using GitHub Copilot.

---

## 🎯 Prompt 1: Game Concept & Core Data Model
> **Prompt:**  
> *"I want to build an engaging, screen-free terminal 'Choose Your Own Adventure' RPG in Python for MLH Hacktoberfest. The theme is a developer trapped inside a 4.8-million-line legacy monolithic codebase ('The Monolith'). Design a clean object-oriented `Player` model in `src/player.py` tracking:  
> - `sanity` (HP, ranges 0-100)  
> - `coffee` (Energy/Mana, used for actions like unit tests)  
> - `stars` (Currency, earned from refactoring)  
> - Equipment (Weapon, Armor with damage/defense bonuses)  
> - Inventory list with consumables and special items  
> - Game progress boolean flags for branching story checks  
> Include full JSON serialization (`to_dict` and `from_dict`) for clean save/load functionality."*

### 🛠️ Copilot Output & Refinements:
- Generated the `Player` class in [`src/player.py`](./src/player.py).
- Engineered defense mitigation calculus: `max(1, amount - self.defense_bonus)`.
- Added leveled scaling: increasing Max Sanity (+15) and Max Coffee (+10) upon reaching XP thresholds.

---

## 🎯 Prompt 2: Combat Engine & Software Engineering Mechanics
> **Prompt:**  
> *"Create a tactical turn-based combat system in `src/combat.py` where the player battles software bugs ('Null Pointer Goblin', 'Race Condition Chimera', 'Memory Leak Dragon'). Instead of generic fantasy spells, ground all actions in real developer workflows:  
> 1. 'Git Blame Strike' (Standard weapon attack)  
> 2. 'Unit Test Barrier' (Consumes coffee; deploys CI shield + heals sanity for 2 turns)  
> 3. 'Hotfix Overclock' (Consumes coffee; high burst damage with critical strike chance)  
> 4. Consumable items (Drinking Triple Espresso or reading Git Cheatsheet)  
> 5. 'Git Stash' (Flee encounter with probability roll)  
> Provide clear visual feedback and handle victory/defeat state transitions."*

### 🛠️ Copilot Output & Refinements:
- Generated `run_battle(player, enemy)` and `Enemy` class in [`src/combat.py`](./src/combat.py).
- Balanced coffee cost vs. combat durability so players must manage their resource budget between chapters.

---

## 🎯 Prompt 3: Narrative Branching & Multiple Endings
> **Prompt:**  
> *"Author an interactive branching narrative in `src/story.py` across 3 chambers:  
> - Chamber 1: The Gateway of Dependencies (Chamber of Global State vs. Crypt of Deprecated Libraries)  
> - Chamber 2: The Race Condition Labyrinth (Thread synchronization puzzles with coffee/mutex options)  
> - Chamber 3: The Core of the Monolith (Boss battle against the Memory Leak Dragon)  
> - Epilogue: 3 unique endings reflecting tech career philosophies (The Microservice Ascension, The Pragmatic Modular Monolith, and The Hacktoberfest Legend: Touching Grass outdoors).  
> Wire in story flags and checkpoint menus between chambers."*

### 🛠️ Copilot Output & Refinements:
- Structured chapter functions (`chapter_1_gateway`, `chapter_2_labyrinth`, `chapter_3_boss`, `epilogue`).
- Connected loot and narrative flags (`defeated_null_pointer`, `monolith_core_unlocked`) to inventory rewards.

---

## 🎯 Prompt 4: Terminal UI, Zero-Dependency Design, and Unit Testing
> **Prompt:**  
> *"Implement terminal visual enhancements in `src/ui.py` using ANSI color codes and unicode progress bars for health/coffee meters. Ensure the application requires zero external pip dependencies so any MLH judge can clone and run it immediately with `python main.py`. Then write a comprehensive pytest suite in `tests/test_game.py` verifying player stats, damage formulas, inventory operations, and serialization."*

### 🛠️ Copilot Output & Refinements:
- Implemented `render_bar()` with dynamic block characters `█` and `░`.
- Built 7 comprehensive unit tests in [`tests/test_game.py`](./tests/test_game.py) achieving 100% test pass in 0.11s.

---

## 🏆 Takeaways from Building with GitHub Copilot
1. **Rapid Prototyping:** Copilot drastically accelerated drafting repetitive data models, CLI menus, and combat damage algorithms.
2. **Thematic Coherence:** By providing specific engineering context in the prompts, Copilot generated humorous, relatable developer tropes and narrative dialogue.
3. **Robust Reliability:** Unit testing paired with AI generation caught edge cases early (e.g. sanity overflowing max health, inventory removal down to zero quantity).
