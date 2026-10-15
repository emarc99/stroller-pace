"""
Branching narrative tree and encounters for Escape the Legacy Monolith.
"""

import time
from .ui import Colors, type_text, select_choice, print_status_hud
from .combat import Enemy, run_battle

def scene_intro(player):
    type_text("\n[YEAR 2026: HACKTOBERFEST EXPEDITION]", 0.02, Colors.CYAN)
    type_text(
        "You step into the subterranean server room of an ancient tech giant.\n"
        "Before you looms The Legacy Monolith: 4.8 million lines of unformatted code,\n"
        "zero documentation, and a single deployment script named 'do_not_touch.sh'.",
        0.015
    )
    time.sleep(0.5)

def chapter_1_gateway(player):
    print_status_hud(player)
    type_text(
        "\nYou find yourself standing at the Gateway of Dependencies.\n"
        "Two massive corridors branch ahead into darkness:\n"
        "Left: The Chamber of Global State (a damp hallway smelling of mutable variables).\n"
        "Right: The Crypt of Deprecated Libraries (littered with broken npm packages).",
        0.015
    )

    choice = select_choice("Where do you venture first?", [
        "Explore the Chamber of Global State",
        "Investigate the Crypt of Deprecated Libraries",
        "Inspect the server rack near the door"
    ])

    if choice == 1:
        type_text("\nYou wade through unindexed global arrays...", 0.015)
        enemy = Enemy(
            name="Null Pointer Goblin",
            hp=45,
            attack=12,
            xp_reward=60,
            stars_reward=15,
            lore="Spawns whenever developers forget to validate input arguments."
        )
        if not run_battle(player, enemy):
            return False
        player.flags["defeated_null_pointer"] = True
        player.add_item("strict_null_checker", "Strict Null Compiler Flag", "equipment", 1)
        player.weapon_bonus += 4
        print(f"\n{Colors.GREEN}🎁 Loot acquired: Strict Null Compiler Flag! Weapon bonus increased to +{player.weapon_bonus}!{Colors.RESET}")

    elif choice == 2:
        type_text("\nYou search through the Crypt of Deprecated Libraries...", 0.015)
        type_text("You unearth an intact documentation scroll from 2014!", 0.015, Colors.YELLOW)
        player.flags["discovered_secret_docs"] = True
        player.add_item("coffee_espresso", "Triple Espresso Shot", "consumable", 2, restore_coffee=30)
        player.armor = "Docker Container Isolation Vest"
        player.defense_bonus += 5
        print(f"\n{Colors.GREEN}🛡️ Equipped Docker Container Isolation Vest! Defense increased to +{player.defense_bonus}!{Colors.RESET}")
    
    else:
        type_text("\nYou look behind the server rack and find a hidden coffee stash and a pristine Git log!", 0.015)
        player.stars += 20
        player.restore_energy(25)
        player.add_item("doc_cheatsheet", "Git Interactive Rebase Map", "consumable", 1, restore_sanity=35)
        print(f"\n{Colors.YELLOW}⭐️ Found +20 Stars and restored 25 Coffee!{Colors.RESET}")

    return True

def chapter_2_labyrinth(player):
    print_status_hud(player)
    type_text(
        "\n--- CHAPTER 2: THE RACE CONDITION LABYRINTH ---\n"
        "The corridor twists into an asynchronous nightmare.\n"
        "Threads are spinning wildly without semaphores. Shared memory is glowing radioactive green.",
        0.015
    )

    choice = select_choice("How do you stabilize the asynchronous loop?", [
        "Deploy a Mutex Lock & Semaphore Barrier (Requires 15 Coffee)",
        "Attempt manual thread synchronization (Risky dice roll)",
        "Engage the Race Condition Chimera in combat"
    ])

    if choice == 1:
        if player.use_coffee(15):
            type_text(
                "\n🔒 You lock down critical shared memory buffers!\n"
                "The threads align in harmonic synchronization. The path clears smoothly!",
                0.015,
                Colors.CYAN
            )
            player.add_xp(80)
            player.stars += 15
        else:
            type_text("\n☕ You didn't have enough coffee! The threads collapse into chaos!", 0.015, Colors.RED)
            player.take_damage(20)

    elif choice == 2:
        type_text("\nYou frantically reorder async callbacks...", 0.015)
        import random
        if random.random() > 0.4:
            type_text("Success! The event loop clears without deadlock!", 0.015, Colors.GREEN)
            player.add_xp(100)
            player.stars += 25
        else:
            type_text("Deadlock detected! You lose 18 Sanity in debugging stress!", 0.015, Colors.RED)
            player.take_damage(18)

    else:
        enemy = Enemy(
            name="Race Condition Chimera",
            hp=65,
            attack=16,
            xp_reward=120,
            stars_reward=30,
            lore="Feeds on unsynchronized writes and intermittent test failures."
        )
        if not run_battle(player, enemy):
            return False

    player.flags["refactored_spaghetti_hall"] = True
    return True

def chapter_3_boss(player):
    print_status_hud(player)
    type_text(
        "\n=======================================================\n"
        "--- CHAPTER 3: THE CORE OF THE LEGACY MONOLITH ---\n"
        "You step into the central chamber. The cooling fans shriek at maximum RPM.\n"
        "Hovering over the mainframe is the final abomination:\n"
        "THE MEMORY LEAK DRAGON (V8 Heap Exhaustion Spectre)\n"
        "=======================================================",
        0.015,
        Colors.RED
    )

    enemy = Enemy(
        name="Memory Leak Dragon",
        hp=95,
        attack=22,
        xp_reward=250,
        stars_reward=100,
        lore="Devourer of RAM, slayer of Kubernetes pods, terror of Sunday deployments."
    )

    if not run_battle(player, enemy):
        return False

    player.flags["monolith_core_unlocked"] = True
    return True

def epilogue(player):
    type_text(
        "\n✨ THE CORE HAS FALLEN! The server fans decelerate to a peaceful whisper.\n"
        "On the main terminal, three deployment keys are flashing:\n",
        0.015,
        Colors.GREEN
    )

    choice = select_choice("How do you choose to refactor the future?", [
        "Ending 1: The Microservice Ascension (Containerize everything into Kubernetes)",
        "Ending 2: The Pragmatic Modular Monolith (Clean domain-driven modular boundaries)",
        "Ending 3: The Open-Source Hacktoberfest Legend (Publish the code & touch grass!)"
    ])

    if choice == 1:
        type_text(
            f"\n🏆 ENDING 1: MICROSERVICE ASCENSION\n"
            f"{player.name} split the monolith into 42 microservices.\n"
            f"Your cloud bill is $40,000/month, but you have 100% uptime and a Grafana dashboard that looks like Star Wars.\n"
            f"Final Score: {player.stars} Stars | Level {player.level}",
            0.015,
            Colors.CYAN
        )
    elif choice == 2:
        type_text(
            f"\n🏆 ENDING 2: PRAGMATIC MODULAR MONOLITH\n"
            f"{player.name} rewrote the codebase into a clean, decoupled modular monolith.\n"
            f"Build times dropped to 3 seconds. The team named the conference room after you.\n"
            f"Final Score: {player.stars} Stars | Level {player.level}",
            0.015,
            Colors.GREEN
        )
    else:
        type_text(
            f"\n🏆 ENDING 3: THE TRUE HACKTOBERFEST LEGEND\n"
            f"{player.name} committed the final pull request, closed the laptop,\n"
            f"walked outside into the park, and Touched Grass under the October sky.\n"
            f"Final Score: {player.stars} Stars | Level {player.level}",
            0.015,
            Colors.YELLOW
        )
