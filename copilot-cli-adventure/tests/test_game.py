"""
Unit tests for Escape the Legacy Monolith.
Verifies player mechanics, combat calculation, inventory handling, and save/load serialization.
"""

import sys
import os
import pytest

# Ensure parent path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.player import Player
from src.combat import Enemy

def test_player_initialization():
    p = Player(name="AliceCoder")
    assert p.name == "AliceCoder"
    assert p.sanity == 100
    assert p.max_sanity == 100
    assert p.coffee == 50
    assert p.level == 1
    assert p.is_alive() is True

def test_damage_and_healing():
    p = Player(name="Bob")
    # Take damage accounting for defense bonus (2)
    taken = p.take_damage(20)
    assert taken == 18
    assert p.sanity == 82

    # Healing
    healed = p.heal(10)
    assert healed == 10
    assert p.sanity == 92

    # Cannot exceed max sanity
    healed_overflow = p.heal(50)
    assert p.sanity == 100
    assert healed_overflow == 8

def test_coffee_energy_usage():
    p = Player(name="Charlie")
    assert p.use_coffee(20) is True
    assert p.coffee == 30
    assert p.use_coffee(40) is False
    assert p.coffee == 30
    p.restore_energy(15)
    assert p.coffee == 45

def test_inventory_management():
    p = Player(name="Dana")
    # Initial inventory has items
    assert len(p.inventory) > 0
    p.add_item("potion_red", "Red Bull Elixir", "consumable", qty=3)
    
    # Check item exists
    found = [i for i in p.inventory if i["id"] == "potion_red"]
    assert len(found) == 1
    assert found[0]["qty"] == 3

    # Remove item
    assert p.remove_item("potion_red", 2) is True
    assert found[0]["qty"] == 1
    assert p.remove_item("potion_red", 1) is True
    assert len([i for i in p.inventory if i["id"] == "potion_red"]) == 0

def test_level_up_mechanics():
    p = Player(name="Evan")
    assert p.level == 1
    leveled = p.add_xp(120)
    assert leveled is True
    assert p.level == 2
    assert p.max_sanity == 115
    assert p.sanity == 115
    assert p.max_coffee == 60
    assert p.xp == 20

def test_save_load_serialization():
    p = Player(name="Fiona")
    p.sanity = 64
    p.coffee = 22
    p.stars = 150
    p.weapon = "Mechanical Keyboard with Blue Switches"
    p.weapon_bonus = 12
    p.flags["defeated_null_pointer"] = True

    data = p.to_dict()
    loaded = Player.from_dict(data)

    assert loaded.name == "Fiona"
    assert loaded.sanity == 64
    assert loaded.coffee == 22
    assert loaded.stars == 150
    assert loaded.weapon == "Mechanical Keyboard with Blue Switches"
    assert loaded.weapon_bonus == 12
    assert loaded.flags["defeated_null_pointer"] is True

def test_enemy_mechanics():
    e = Enemy(name="BugBoss", hp=50, attack=15, xp_reward=80, stars_reward=20, lore="Test enemy")
    assert e.is_alive() is True
    e.take_damage(30)
    assert e.hp == 20
    assert e.is_alive() is True
    e.take_damage(25)
    assert e.hp == 0
    assert e.is_alive() is False
