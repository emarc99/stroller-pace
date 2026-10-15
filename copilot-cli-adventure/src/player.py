"""
Player state management for Escape the Legacy Monolith.
Tracks sanity (HP), coffee (Mana/Stamina), stars (Currency), inventory, and equipment.
"""

from typing import Dict, List, Optional

class Player:
    def __init__(self, name: str = "DevHacker"):
        self.name = name
        self.max_sanity: int = 100
        self.sanity: int = 100
        self.max_coffee: int = 50
        self.coffee: int = 50
        self.stars: int = 25
        self.level: int = 1
        self.xp: int = 0
        self.weapon: str = "Rubber Duck Debugger"
        self.weapon_bonus: int = 5
        self.armor: str = "T-Shirt with Tech Conference Logo"
        self.defense_bonus: int = 2
        self.inventory: List[Dict[str, any]] = [
            {"id": "coffee_espresso", "name": "Triple Espresso Shot", "type": "consumable", "restore_coffee": 30, "qty": 2},
            {"id": "doc_cheatsheet", "name": "Cheat Sheet of Git Wisdom", "type": "consumable", "restore_sanity": 25, "qty": 1},
            {"id": "stack_overflow_token", "name": "StackOverflow Green Checkmark", "type": "special", "qty": 1}
        ]
        self.flags: Dict[str, bool] = {
            "has_container_shield": False,
            "refactored_spaghetti_hall": False,
            "defeated_null_pointer": False,
            "discovered_secret_docs": False,
            "monolith_core_unlocked": False
        }

    def is_alive(self) -> bool:
        return self.sanity > 0

    def take_damage(self, amount: int) -> int:
        effective_damage = max(1, amount - self.defense_bonus)
        self.sanity = max(0, self.sanity - effective_damage)
        return effective_damage

    def heal(self, amount: int) -> int:
        prev = self.sanity
        self.sanity = min(self.max_sanity, self.sanity + amount)
        return self.sanity - prev

    def restore_energy(self, amount: int) -> int:
        prev = self.coffee
        self.coffee = min(self.max_coffee, self.coffee + amount)
        return self.coffee - prev

    def use_coffee(self, cost: int) -> bool:
        if self.coffee >= cost:
            self.coffee -= cost
            return True
        return False

    def add_item(self, item_id: str, name: str, item_type: str, qty: int = 1, **kwargs):
        for item in self.inventory:
            if item["id"] == item_id:
                item["qty"] += qty
                return
        new_item = {"id": item_id, "name": name, "type": item_type, "qty": qty}
        new_item.update(kwargs)
        self.inventory.append(new_item)

    def remove_item(self, item_id: str, qty: int = 1) -> bool:
        for item in self.inventory:
            if item["id"] == item_id:
                if item["qty"] >= qty:
                    item["qty"] -= qty
                    if item["qty"] == 0:
                        self.inventory.remove(item)
                    return True
                return False
        return False

    def add_xp(self, amount: int) -> bool:
        self.xp += amount
        needed = self.level * 100
        if self.xp >= needed:
            self.level += 1
            self.xp -= needed
            self.max_sanity += 15
            self.sanity = self.max_sanity
            self.max_coffee += 10
            self.coffee = self.max_coffee
            return True
        return False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "max_sanity": self.max_sanity,
            "sanity": self.sanity,
            "max_coffee": self.max_coffee,
            "coffee": self.coffee,
            "stars": self.stars,
            "level": self.level,
            "xp": self.xp,
            "weapon": self.weapon,
            "weapon_bonus": self.weapon_bonus,
            "armor": self.armor,
            "defense_bonus": self.defense_bonus,
            "inventory": self.inventory,
            "flags": self.flags
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        player = cls(name=data.get("name", "DevHacker"))
        player.max_sanity = data.get("max_sanity", 100)
        player.sanity = data.get("sanity", 100)
        player.max_coffee = data.get("max_coffee", 50)
        player.coffee = data.get("coffee", 50)
        player.stars = data.get("stars", 25)
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)
        player.weapon = data.get("weapon", "Rubber Duck Debugger")
        player.weapon_bonus = data.get("weapon_bonus", 5)
        player.armor = data.get("armor", "T-Shirt with Tech Conference Logo")
        player.defense_bonus = data.get("defense_bonus", 2)
        player.inventory = data.get("inventory", [])
        player.flags = data.get("flags", {})
        return player
