#!/usr/bin/env python3
"""
Adventure Quest - Text-Based Multiplayer Adventure Game
Items and Inventory Module
Contributed by: Varshith
"""

import json
import random
import time
from typing import Dict, List, Optional, Any, Union, Tuple


class Item:
    """Base class for all items in the game"""
    def __init__(self, name: str, description: str, value: int = 0):
        self.name = name
        self.description = description
        self.value = value  # Value in gold
        self.weight = 1.0
        self.rarity = "Common"  # Common, Uncommon, Rare, Epic, Legendary
        self.type = "Miscellaneous"
        self.can_be_equipped = False
        self.can_be_used = False
        self.can_be_sold = True
        self.can_be_dropped = True
        self.quantity = 1
        self.max_stack = 99
        self.unique_id = f"{name.lower().replace(' ', '_')}_{random.randint(1000, 9999)}"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.rarity}): {self.description}"
    
    def use(self, player: Any) -> Tuple[bool, str]:
        """Use the item. Override in subclasses."""
        if not self.can_be_used:
            return False, f"The {self.name} cannot be used."
        return False, "Nothing happens."
    
    def set_rarity(self, rarity: str) -> None:
        """Set the rarity of the item"""
        valid_rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]
        if rarity in valid_rarities:
            self.rarity = rarity
            # Adjust value based on rarity
            rarity_multipliers = {
                "Common": 1,
                "Uncommon": 2,
                "Rare": 5,
                "Epic": 10,
                "Legendary": 25
            }
            self.value = self.value * rarity_multipliers[rarity]
    
    def stack(self, quantity: int = 1) -> bool:
        """Add quantity to this item's stack if possible"""
        if self.quantity + quantity <= self.max_stack:
            self.quantity += quantity
            return True
        return False
    
    def split_stack(self, quantity: int = 1) -> Optional['Item']:
        """Split this stack and return a new item with the specified quantity"""
        if quantity <= 0 or quantity >= self.quantity:
            return None
        
        new_item = self.__class__(self.name, self.description, self.value)
        new_item.quantity = quantity
        self.quantity -= quantity
        return new_item
    
    def get_full_description(self) -> str:
        """Get a detailed description of the item"""
        desc = f"{self.name} ({self.rarity})\n"
        desc += f"Type: {self.type}\n"
        desc += f"{self.description}\n"
        desc += f"Value: {self.value} gold\n"
        desc += f"Weight: {self.weight}\n"
        
        if self.quantity > 1:
            desc += f"Quantity: {self.quantity}\n"
        
        return desc
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert item to dictionary for saving"""
        return {
            "name": self.name,
            "description": self.description,
            "value": self.value,
            "weight": self.weight,
            "rarity": self.rarity,
            "type": self.type,
            "can_be_equipped": self.can_be_equipped,
            "can_be_used": self.can_be_used,
            "can_be_sold": self.can_be_sold,
            "can_be_dropped": self.can_be_dropped,
            "quantity": self.quantity,
            "max_stack": self.max_stack,
            "unique_id": self.unique_id,
            "item_class": self.__class__.__name__
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Item':
        """Create item from dictionary data"""
        item = cls(data["name"], data["description"], data["value"])
        item.weight = data["weight"]
        item.rarity = data["rarity"]
        item.type = data["type"]
        item.can_be_equipped = data["can_be_equipped"]
        item.can_be_used = data["can_be_used"]
        item.can_be_sold = data["can_be_sold"]
        item.can_be_dropped = data["can_be_dropped"]
        item.quantity = data["quantity"]
        item.max_stack = data["max_stack"]
        item.unique_id = data["unique_id"]
        return item


class Weapon(Item):
    """Class for weapon items that can be equipped"""
    def __init__(self, name: str, description: str, value: int = 10, damage: int = 5):
        super().__init__(name, description, value)
        self.damage = damage
        self.type = "Weapon"
        self.can_be_equipped = True
        self.weight = 2.0
        self.equip_slot = "Weapon"
        self.two_handed = False
        self.weapon_type = "Sword"  # Sword, Axe, Mace, Dagger, Staff, Bow, etc.
        self.range = "Melee"  # Melee or Ranged
        self.durability = 100
        self.max_durability = 100
        self.attributes = {}  # Additional weapon attributes
    
    def get_damage(self) -> int:
        """Get the damage value of the weapon"""
        # Apply durability scaling (weapons do less damage as they break)
        durability_factor = self.durability / self.max_durability
        if durability_factor < 0.5:
            return int(self.damage * durability_factor)
        return self.damage
    
    def degrade(self, amount: int = 1) -> bool:
        """Reduce weapon durability by using it"""
        self.durability -= amount
        if self.durability <= 0:
            self.durability = 0
            return True  # Weapon broke
        return False
    
    def repair(self, amount: int = 10) -> None:
        """Repair the weapon"""
        self.durability += amount
        if self.durability > self.max_durability:
            self.durability = self.max_durability
    
    def get_full_description(self) -> str:
        """Get a detailed description of the weapon"""
        desc = super().get_full_description()
        desc += f"Damage: {self.get_damage()}\n"
        desc += f"Weapon Type: {self.weapon_type}\n"
        desc += f"Range: {self.range}\n"
        desc += f"Durability: {self.durability}/{self.max_durability}\n"
        
        if self.attributes:
            desc += "Attributes:\n"
            for attr, value in self.attributes.items():
                desc += f"  {attr}: {value}\n"
        
        return desc
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert weapon to dictionary for saving"""
        data = super().to_dict()
        data.update({
            "damage": self.damage,
            "equip_slot": self.equip_slot,
            "two_handed": self.two_handed,
            "weapon_type": self.weapon_type,
            "range": self.range,
            "durability": self.durability,
            "max_durability": self.max_durability,
            "attributes": self.attributes
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Weapon':
        """Create weapon from dictionary data"""
        weapon = super().from_dict(data)
        weapon.damage = data["damage"]
        weapon.equip_slot = data["equip_slot"]
        weapon.two_handed = data["two_handed"]
        weapon.weapon_type = data["weapon_type"]
        weapon.range = data["range"]
        weapon.durability = data["durability"]
        weapon.max_durability = data["max_durability"]
        weapon.attributes = data["attributes"]
        return weapon


class Armor(Item):
    """Class for armor items that can be equipped"""
    def __init__(self, name: str, description: str, value: int = 15, defense: int = 3):
        super().__init__(name, description, value)
        self.defense = defense
        self.type = "Armor"
        self.can_be_equipped = True
        self.weight = 3.0
        self.equip_slot = "Body"  # Head, Body, Legs, Feet, Hands
        self.armor_type = "Light"  # Light, Medium, Heavy
        self.durability = 100
        self.max_durability = 100
        self.attributes = {}  # Additional armor attributes
    
    def get_defense(self) -> int:
        """Get the defense value of the armor"""
        # Apply durability scaling
        durability_factor = self.durability / self.max_durability
        if durability_factor < 0.5:
            return int(self.defense * durability_factor)
        return self.defense
    
    def degrade(self, amount: int = 1) -> bool:
        """Reduce armor durability by taking damage"""
        self.durability -= amount
        if self.durability <= 0:
            self.durability = 0
            return True  # Armor broke
        return False
    
    def repair(self, amount: int = 10) -> None:
        """Repair the armor"""
        self.durability += amount
        if self.durability > self.max_durability:
            self.durability = self.max_durability
    
    def get_full_description(self) -> str:
        """Get a detailed description of the armor"""
        desc = super().get_full_description()
        desc += f"Defense: {self.get_defense()}\n"
        desc += f"Armor Type: {self.armor_type}\n"
        desc += f"Equip Slot: {self.equip_slot}\n"
        desc += f"Durability: {self.durability}/{self.max_durability}\n"
        
        if self.attributes:
            desc += "Attributes:\n"
            for attr, value in self.attributes.items():
                desc += f"  {attr}: {value}\n"
        
        return desc
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert armor to dictionary for saving"""
        data = super().to_dict()
        data.update({
            "defense": self.defense,
            "equip_slot": self.equip_slot,
            "armor_type": self.armor_type,
            "durability": self.durability,
            "max_durability": self.max_durability,
            "attributes": self.attributes
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Armor':
        """Create armor from dictionary data"""
        armor = super().from_dict(data)
        armor.defense = data["defense"]
        armor.equip_slot = data["equip_slot"]
        armor.armor_type = data["armor_type"]
        armor.durability = data["durability"]
        armor.max_durability = data["max_durability"]
        armor.attributes = data["attributes"]
        return armor


class Potion(Item):
    """Class for consumable potion items"""
    def __init__(self, name: str, description: str, value: int = 5, effect_amount: int = 20):
        super().__init__(name, description, value)
        self.effect_amount = effect_amount
        self.type = "Potion"
        self.can_be_used = True
        self.weight = 0.5
        self.max_stack = 10
        self.effect_type = "Health"  # Health, Mana, Strength, etc.
        self.effect_duration = 0  # 0 for instant, >0 for duration in seconds
    
    def use(self, player: Any) -> Tuple[bool, str]:
        """Use the potion on a player"""
        if self.quantity <= 0:
            return False, "You don't have any of this item left."
        
        if self.effect_type == "Health":
            if player.health >= player.max_health:
                return False, "Your health is already full."
            healed = player.heal(self.effect_amount)
            self.quantity -= 1
            return True, f"You used {self.name} and restored {healed} health."
            
        elif self.effect_type == "Mana":
            if player.mana >= player.max_mana:
                return False, "Your mana is already full."
            restored = player.restore_mana(self.effect_amount)
            self.quantity -= 1
            return True, f"You used {self.name} and restored {restored} mana."
            
        elif self.effect_type == "Strength":
            # Temporary strength buff
            player.attack += self.effect_amount
            self.quantity -= 1
            
            # Schedule buff removal after duration
            # In a real game, this would use a proper buff/debuff system
            print(f"Your strength has been increased by {self.effect_amount} for {self.effect_duration} seconds.")
            
            return True, f"You used {self.name} and gained {self.effect_amount} strength for {self.effect_duration} seconds."
        
        return False, "This potion has no effect."
    
    def get_full_description(self) -> str:
        """Get a detailed description of the potion"""
        desc = super().get_full_description()
        desc += f"Effect: {self.effect_type}\n"
        desc += f"Amount: {self.effect_amount}\n"
        
        if self.effect_duration > 0:
            desc += f"Duration: {self.effect_duration} seconds\n"
        else:
            desc += "Duration: Instant\n"
        
        return desc
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert potion to dictionary for saving"""
        data = super().to_dict()
        data.update({
            "effect_amount": self.effect_amount,
            "effect_type": self.effect_type,
            "effect_duration": self.effect_duration
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Potion':
        """Create potion from dictionary data"""
        potion = super().from_dict(data)
        potion.effect_amount = data["effect_amount"]
        potion.effect_type = data["effect_type"]
        potion.effect_duration = data["effect_duration"]
        return potion


class QuestItem(Item):
    """Class for special quest-related items"""
    def __init__(self, name: str, description: str, quest_id: str):
        super().__init__(name, description, 0)  # Quest items have no value
        self.quest_id = quest_id
        self.type = "Quest Item"
        self.can_be_sold = False
        self.can_be_dropped = False
        self.max_stack = 1
    
    def get_full_description(self) -> str:
        """Get a detailed description of the quest item"""
        desc = super().get_full_description()
        desc += "This item is needed for a quest.\n"
        return desc
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quest item to dictionary for saving"""
        data = super().to_dict()
        data.update({
            "quest_id": self.quest_id
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuestItem':
        """Create quest item from dictionary data"""
        item = super().from_dict(data)
        item.quest_id = data["quest_id"]
        return item


class ItemFactory:
    """Factory class for creating different types of items"""
    @staticmethod
    def create_item(item_data: Dict[str, Any]) -> Item:
        """Create an item based on item data"""
        item_class = item_data.get("item_class", "Item")
        
        if item_class == "Weapon":
            return Weapon.from_dict(item_data)
        elif item_class == "Armor":
            return Armor.from_dict(item_data)
        elif item_class == "Potion":
            return Potion.from_dict(item_data)
        elif item_class == "QuestItem":
            return QuestItem.from_dict(item_data)
        else:
            return Item.from_dict(item_data)
    
    @staticmethod
    def create_random_weapon(level: int = 1, rarity: str = None) -> Weapon:
        """Create a random weapon appropriate for a given level"""
        weapon_types = ["Sword", "Axe", "Mace", "Dagger", "Staff", "Bow"]
        weapon_type = random.choice(weapon_types)
        
        prefixes = ["Sharp", "Sturdy", "Rusty", "Ancient", "Glimmering", "Heavy", "Light"]
        prefix = random.choice(prefixes)
        
        name = f"{prefix} {weapon_type}"
        description = f"A {prefix.lower()} {weapon_type.lower()} that looks {random.choice(['well-crafted', 'ordinary', 'unusual', 'reliable'])}."
        
        # Base damage scaled to level
        base_damage = 5 + (level * 2)
        # Random variation
        damage_variation = random.randint(-2, 3)
        damage = max(1, base_damage + damage_variation)
        
        # Value based on damage and level
        value = damage * 2 + (level * 5)
        
        weapon = Weapon(name, description, value, damage)
        weapon.weapon_type = weapon_type
        
        if weapon_type in ["Bow", "Staff"]:
            weapon.range = "Ranged"
        
        if weapon_type in ["Axe", "Staff"]:
            weapon.two_handed = True
        
        # Set rarity if specified, otherwise random based on level
        if rarity:
            weapon.set_rarity(rarity)
        else:
            rarities = ["Common", "Common", "Common", "Uncommon", "Uncommon", "Rare", "Epic", "Legendary"]
            weights = [50, 50, 50, 25, 25, 10, 3, 1]
            # Adjust weights based on level
            for i in range(min(level, 7)):
                weights[i] = max(1, weights[i] - 5)
                weights[i+1] += 5
            
            selected_rarity = random.choices(rarities, weights=weights, k=1)[0]
            weapon.set_rarity(selected_rarity)
        
        # Add random attributes based on rarity
        attribute_chance = {"Common": 0.1, "Uncommon": 0.3, "Rare": 0.6, "Epic": 0.9, "Legendary": 1.0}
        max_attributes = {"Common": 0, "Uncommon": 1, "Rare": 2, "Epic": 3, "Legendary": 4}
        
        if random.random() < attribute_chance[weapon.rarity]:
            num_attributes = random.randint(0, max_attributes[weapon.rarity])
            possible_attributes = ["critical_chance", "attack_speed", "lifesteal", "fire_damage", "ice_damage"]
            
            for _ in range(num_attributes):
                attr = random.choice(possible_attributes)
                value = random.randint(1, 5 + level)
                weapon.attributes[attr] = value
        
        return weapon
    
    @staticmethod
    def create_random_armor(level: int = 1, rarity: str = None) -> Armor:
        """Create a random armor appropriate for a given level"""
        armor_types = ["Light", "Medium", "Heavy"]
        armor_type = random.choice(armor_types)
        
        slot_types = ["Head", "Body", "Legs", "Feet", "Hands"]
        slot = random.choice(slot_types)
        
        slot_names = {
            "Head": ["Helmet", "Cap", "Hood"],
            "Body": ["Chestplate", "Tunic", "Robe"],
            "Legs": ["Leggings", "Pants", "Greaves"],
            "Feet": ["Boots", "Shoes", "Sandals"],
            "Hands": ["Gloves", "Gauntlets", "Bracers"]
        }
        
        material_by_type = {
            "Light": ["Leather", "Cloth", "Hide"],
            "Medium": ["Chainmail", "Scale", "Bone"],
            "Heavy": ["Iron", "Steel", "Plate"]
        }
        
        material = random.choice(material_by_type[armor_type])
        item_name = random.choice(slot_names[slot])
        
        name = f"{material} {item_name}"
        description = f"{armor_type} armor for your {slot.lower()}. Made of {material.lower()}."
        
        # Base defense scaled to level and armor type
        type_multiplier = {"Light": 0.8, "Medium": 1.0, "Heavy": 1.2}
        base_defense = 3 + int(level * 1.5 * type_multiplier[armor_type])
        
        # Random variation
        defense_variation = random.randint(-1, 2)
        defense = max(1, base_defense + defense_variation)
        
        # Value based on defense and level
        value = defense * 3 + (level * 5)
        
        armor = Armor(name, description, value, defense)
        armor.armor_type = armor_type
        armor.equip_slot = slot
        
        # Set weight based on armor type
        weight_by_type = {"Light": 2.0, "Medium": 3.0, "Heavy": 4.0}
        armor.weight = weight_by_type[armor_type]
        
        # Set rarity if specified, otherwise random based on level
        if rarity:
            armor.set_rarity(rarity)
        else:
            rarities = ["Common", "Common", "Common", "Uncommon", "Uncommon", "Rare", "Epic", "Legendary"]
            weights = [50, 50, 50, 25, 25, 10, 3, 1]
            # Adjust weights based on level
            for i in range(min(level, 7)):
                weights[i] = max(1, weights[i] - 5)
                weights[i+1] += 5
            
            selected_rarity = random.choices(rarities, weights=weights, k=1)[0]
            armor.set_rarity(selected_rarity)
        
        # Add random attributes based on rarity
        attribute_chance = {"Common": 0.1, "Uncommon": 0.3, "Rare": 0.6, "Epic": 0.9, "Legendary": 1.0}
        max_attributes = {"Common": 0, "Uncommon": 1, "Rare": 2, "Epic": 3, "Legendary": 4}
        
        if random.random() < attribute_chance[armor.rarity]:
            num_attributes = random.randint(0, max_attributes[armor.rarity])
            possible_attributes = ["health_bonus", "mana_bonus", "stamina", "resistance", "movement_speed"]
            
            for _ in range(num_attributes):
                attr = random.choice(possible_attributes)
                value = random.randint(1, 5 + level)
                armor.attributes[attr] = value
        
        return armor
    
    @staticmethod
    def create_random_potion(level: int = 1) -> Potion:
        """Create a random potion appropriate for a given level"""
        potion_types = ["Health", "Mana", "Strength", "Speed", "Resistance"]
        potion_type = random.choice(potion_types)
        
        name = f"{potion_type} Potion"
        description = f"A potion that restores {potion_type.lower()}."
        
        # Base effect amount scaled to level
        base_amount = 20 + (level * 10)
        # Random variation
        amount_variation = random.randint(-5, 10)
        effect_amount = max(10, base_amount + amount_variation)
        
        # Value based on effect amount and level
        value = int(effect_amount / 4) + (level * 2)
        
        potion = Potion(name, description, value, effect_amount)
        potion.effect_type = potion_type
        
        # Set duration for some potion types
        if potion_type in ["Strength", "Speed", "Resistance"]:
            potion.effect_duration = 30 + (level * 10)  # Duration in seconds
        
        return potion


class Inventory:
    """Class for managing a player's inventory"""
    def __init__(self, max_weight: float = 50.0):
        self.items = []
        self.max_weight = max_weight
        self.equipped_items = {
            "Weapon": None,
            "Head": None,
            "Body": None,
            "Legs": None,
            "Feet": None,
            "Hands": None,
            "Accessory1": None,
            "Accessory2": None
        }
    
    def add_item(self, item: Item) -> Tuple[bool, str]:
        """
        Add an item to the inventory
        Returns (success, message)
        """
        # Check if adding would exceed weight limit
        if self.get_total_weight() + (item.weight * item.quantity) > self.max_weight:
            return False, "Your inventory is too heavy to carry this item."
        
        # Check if a similar stackable item already exists
        if item.quantity > 1 or item.max_stack > 1:
            for existing_item in self.items:
                if (existing_item.name == item.name and 
                    existing_item.__class__.__name__ == item.__class__.__name__ and
                    existing_item.quantity < existing_item.max_stack):
                    
                    # Calculate how many items can be added to the stack
                    space_in_stack = existing_item.max_stack - existing_item.quantity
                    to_add = min(item.quantity, space_in_stack)
                    
                    existing_item.quantity += to_add
                    item.quantity -= to_add
                    
                    # If all items were added to existing stack
                    if item.quantity == 0:
                        return True, f"Added {to_add} {item.name}(s) to your inventory."
        
        # If we still have items to add, add as a new stack
        if item.quantity > 0:
            self.items.append(item)
            return True, f"Added {item.quantity} {item.name}(s) to your inventory."
        
        return True, "Added to your inventory."
    
    def remove_item(self, item_id: str, quantity: int = 1) -> Tuple[bool, str, Optional[Item]]:
        """
        Remove an item from the inventory by its unique ID
        Returns (success, message, removed_item)
        """
        for i, item in enumerate(self.items):
            if item.unique_id == item_id:
                if quantity >= item.quantity:
                    # Remove the entire stack
                    removed_item = self.items.pop(i)
                    return True, f"Removed {removed_item.name} from your inventory.", removed_item
                else:
                    # Remove part of the stack
                    item.quantity -= quantity
                    # Create a new item with the removed quantity
                    removed_item = type(item)(item.name, item.description, item.value)
                    removed_item.quantity = quantity
                    return True, f"Removed {quantity} {item.name}(s) from your inventory.", removed_item
        
        return False, "Item not found in inventory.", None
    
    def remove_item_by_name(self, name: str, quantity: int = 1) -> Tuple[bool, str, Optional[Item]]:
        """
        Remove an item from the inventory by its name
        Returns (success, message, removed_item)
        """
        for i, item in enumerate(self.items):
            if item.name == name:
                if quantity >= item.quantity:
                    # Remove the entire stack
                    removed_item = self.items.pop(i)
                    return True, f"Removed {removed_item.name} from your inventory.", removed_item
                else:
                    # Remove part of the stack
                    item.quantity -= quantity
                    # Create a new item with the removed quantity
                    removed_item = type(item)(item.name, item.description, item.value)
                    removed_item.quantity = quantity
                    return True, f"Removed {quantity} {item.name}(s) from your inventory.", removed_item
        
        return False, f"{name} not found in inventory.", None
    
    def get_item(self, item_id: str) -> Optional[Item]:
        """Get an item from the inventory by its unique ID without removing it"""
        for item in self.items:
            if item.unique_id == item_id:
                return item
        return None
    
    def get_item_by_name(self, name: str) -> Optional[Item]:
        """Get an item from the inventory by its name without removing it"""
        for item in self.items:
            if item.name == name:
                return item
        return None
    
    def use_item(self, item_id: str, player: Any) -> Tuple[bool, str]:
        """Use an item from the inventory"""
        item = self.get_item(item_id)
        if not item:
            return False, "Item not found in inventory."
        
        if not item.can_be_used:
            return False, f"The {item.name} cannot be used."
        
        success, message = item.use(player)
        
        # Remove item if quantity is 0 after use
        if success and item.quantity <= 0:
            self.items = [i for i in self.items if i.unique_id != item_id]
        
        return success, message
    
    def equip_item(self, item_id: str) -> Tuple[bool, str, Optional[Item]]:
        """
        Equip an item from the inventory
        Returns (success, message, unequipped_item)
        """
        item = self.get_item(item_id)
        if not item:
            return False, "Item not found in inventory.", None
        
        if not item.can_be_equipped:
            return False, f"The {item.name} cannot be equipped.", None
        
        # Determine the slot for this item
        slot = "Weapon"
        if hasattr(item, "equip_slot"):
            slot = item.equip_slot
        
        # Check if item is two-handed (weapons only)
        if hasattr(item, "two_handed") and item.two_handed:
            # If equipping a two-handed weapon, also unequip offhand (if implemented)
            pass
        
        # Unequip current item in that slot if any
        unequipped_item = None
        if self.equipped_items[slot]:
            unequipped_item = self.equipped_items[slot]
        
        # Remove the item from inventory
        self.remove_item(item_id)
        
        # Equip the new item
        self.equipped_items[slot] = item
        
        # Add the unequipped item back to inventory if any
        if unequipped_item:
            self.add_item(unequipped_item)
        
        return True, f"Equipped {item.name}.", unequipped_item
    
    def unequip_item(self, slot: str) -> Tuple[bool, str]:
        """Unequip an item from a specific slot"""
        if slot not in self.equipped_items:
            return False, f"Invalid equipment slot: {slot}."
        
        if not self.equipped_items[slot]:
            return False, f"Nothing is equipped in the {slot} slot."
        
        item = self.equipped_items[slot]
        self.equipped_items[slot] = None
        
        # Add the unequipped item to inventory
        success, message = self.add_item(item)
        if not success:
            # If inventory is full, re-equip the item
            self.equipped_items[slot] = item
            return False, "Your inventory is too full to unequip this item."
        
        return True, f"Unequipped {item.name}."
    
    def get_total_weight(self) -> float:
        """Calculate the total weight of all items in the inventory"""
        return sum(item.weight * item.quantity for item in self.items)
    
    def get_equipped_stats(self) -> Dict[str, int]:
        """Calculate combined stats from all equipped items"""
        stats = {
            "attack": 0,
            "defense": 0,
            "attributes": {}
        }
        
        # Add weapon damage
        if self.equipped_items["Weapon"] and hasattr(self.equipped_items["Weapon"], "get_damage"):
            stats["attack"] += self.equipped_items["Weapon"].get_damage()
        
        # Add armor defense
        for slot, item in self.equipped_items.items():
            if item and hasattr(item, "get_defense"):
                stats["defense"] += item.get_defense()
            
            # Combine all attributes from equipped items
            if item and hasattr(item, "attributes"):
                for attr, value in item.attributes.items():
                    if attr in stats["attributes"]:
                        stats["attributes"][attr] += value
                    else:
                        stats["attributes"][attr] = value
        
        return stats
    
    def display(self) -> str:
        """Get a string representation of the inventory"""
        if not self.items:
            return "Your inventory is empty."
        
        result = f"Inventory ({self.get_total_weight():.1f}/{self.max_weight:.1f} weight):\n"
        
        # Group items by type
        items_by_type = {}
        for item in self.items:
            if item.type not in items_by_type:
                items_by_type[item.type] = []
            items_by_type[item.type].append(item)
        
        # Display items by type
        for item_type, items in items_by_type.items():
            result += f"\n{item_type}s:\n"
            for i, item in enumerate(items, 1):
                if item.quantity > 1:
                    result += f"{i}. {item.name} (x{item.quantity}) - {item.description}\n"
                else:
                    result += f"{i}. {item.name} - {item.description}\n"
        
        return result
    
    def display_equipped(self) -> str:
        """Get a string representation of equipped items"""
        result = "Equipped Items:\n"
        
        has_equipped = False
        for slot, item in self.equipped_items.items():
            if item:
                has_equipped = True
                result += f"{slot}: {item.name}\n"
            else:
                result += f"{slot}: Nothing\n"
        
        if not has_equipped:
            result += "You have nothing equipped.\n"
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert inventory to dictionary for saving"""
        return {
            "items": [item.to_dict() for item in self.items],
            "max_weight": self.max_weight,
            "equipped_items": {slot: (item.to_dict() if item else None) for slot, item in self.equipped_items.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Inventory':
        """Create inventory from dictionary data"""
        inventory = cls(data["max_weight"])
        
        # Add items to inventory
        for item_data in data["items"]:
            item = ItemFactory.create_item(item_data)
            inventory.items.append(item)
        
        # Set equipped items
        for slot, item_data in data["equipped_items"].items():
            if item_data:
                inventory.equipped_items[slot] = ItemFactory.create_item(item_data)
        
        return inventory


class Shop:
    """Class representing a shop where items can be bought and sold"""
    def __init__(self, name: str, shop_type: str = "General"):
        self.name = name
        self.shop_type = shop_type  # General, Weapons, Armor, Potions, etc.
        self.items = []
        self.buy_multiplier = 1.0  # Price multiplier when player buys
        self.sell_multiplier = 0.5  # Price multiplier when player sells
        self.gold = 1000
        self.restock_time = 0  # Time until shop restocks
        self.specialty_items = []  # Special items this shop might sell
    
    def add_item(self, item: Item, quantity: int = 1) -> None:
        """Add an item to the shop's inventory"""
        # Check if the item already exists
        for shop_item in self.items:
            if shop_item.name == item.name and shop_item.__class__.__name__ == item.__class__.__name__:
                shop_item.quantity += quantity
                return
        
        # Otherwise add as new item
        new_item = type(item)(item.name, item.description, item.value)
        new_item.quantity = quantity
        self.items.append(new_item)
    
    def remove_item(self, item_id: str, quantity: int = 1) -> Optional[Item]:
        """Remove an item from the shop's inventory"""
        for i, item in enumerate(self.items):
            if item.unique_id == item_id:
                if quantity >= item.quantity:
                    # Remove the entire stack
                    return self.items.pop(i)
                else:
                    # Remove part of the stack
                    item.quantity -= quantity
                    # Create a new item with the removed quantity
                    removed_item = type(item)(item.name, item.description, item.value)
                    removed_item.quantity = quantity
                    return removed_item
        
        return None
    
    def get_buy_price(self, item: Item) -> int:
        """Get the price for a player to buy an item"""
        return int(item.value * self.buy_multiplier)
    
    def get_sell_price(self, item: Item) -> int:
        """Get the price for a player to sell an item"""
        return int(item.value * self.sell_multiplier)
    
    def buy_item(self, player_inventory: Inventory, player_gold: int, item_id: str, quantity: int = 1) -> Tuple[bool, str, int]:
        """
        Player buys an item from the shop
        Returns (success, message, gold_spent)
        """
        # Find the item in shop
        item_to_buy = None
        for item in self.items:
            if item.unique_id == item_id:
                item_to_buy = item
                break
        
        if not item_to_buy:
            return False, "Item not found in shop.", 0
        
        # Check if enough quantity available
        if item_to_buy.quantity < quantity:
            return False, f"Only {item_to_buy.quantity} available.", 0
        
        # Calculate total cost
        total_cost = self.get_buy_price(item_to_buy) * quantity
        
        # Check if player has enough gold
        if player_gold < total_cost:
            return False, "You don't have enough gold.", 0
        
        # Create a copy of the item to add to player's inventory
        purchased_item = type(item_to_buy)(item_to_buy.name, item_to_buy.description, item_to_buy.value)
        purchased_item.quantity = quantity
        
        # Try to add to player's inventory
        success, message = player_inventory.add_item(purchased_item)
        if not success:
            return False, message, 0
        
        # Remove from shop
        item_to_buy.quantity -= quantity
        if item_to_buy.quantity <= 0:
            self.items.remove(item_to_buy)
        
        # Shop gains gold
        self.gold += total_cost
        
        return True, f"Bought {quantity} {purchased_item.name}(s) for {total_cost} gold.", total_cost
    
    def sell_item(self, player_inventory: Inventory, player_gold: int, item_id: str, quantity: int = 1) -> Tuple[bool, str, int]:
        """
        Player sells an item to the shop
        Returns (success, message, gold_earned)
        """
        # Try to remove the item from player's inventory
        success, message, removed_item = player_inventory.remove_item(item_id, quantity)
        if not success or not removed_item:
            return False, message, 0
        
        # Calculate total value
        total_value = self.get_sell_price(removed_item) * removed_item.quantity
        
        # Check if shop has enough gold
        if self.gold < total_value:
            # Return the item to player's inventory
            player_inventory.add_item(removed_item)
            return False, f"The shop doesn't have enough gold ({self.gold}).", 0
        
        # Add the item to shop's inventory
        self.add_item(removed_item, removed_item.quantity)
        
        # Shop loses gold
        self.gold -= total_value
        
        return True, f"Sold {removed_item.quantity} {removed_item.name}(s) for {total_value} gold.", total_value
    
    def restock(self) -> None:
        """Restock the shop with new items"""
        # Add more gold
        self.gold += random.randint(100, 500)
        
        # Add some basic items based on shop type
        if self.shop_type == "General" or self.shop_type == "Potion":
            # Add healing potions
            healing_potion = Potion("Health Potion", "Restores health when consumed.", 15, 30)
            healing_potion.effect_type = "Health"
            self.add_item(healing_potion, random.randint(2, 5))
            
            # Add mana potions
            mana_potion = Potion("Mana Potion", "Restores mana when consumed.", 15, 30)
            mana_potion.effect_type = "Mana"
            self.add_item(mana_potion, random.randint(2, 5))
        
        if self.shop_type == "General" or self.shop_type == "Weapon":
            # Add a couple of random weapons
            for _ in range(random.randint(1, 3)):
                weapon = ItemFactory.create_random_weapon(random.randint(1, 3))
                self.add_item(weapon)
        
        if self.shop_type == "General" or self.shop_type == "Armor":
            # Add a couple of random armor pieces
            for _ in range(random.randint(1, 3)):
                armor = ItemFactory.create_random_armor(random.randint(1, 3))
                self.add_item(armor)
        
        # Add specialty items
        for item_type in self.specialty_items:
            if random.random() < 0.3:  # 30% chance for each specialty item
                if item_type == "weapon":
                    weapon = ItemFactory.create_random_weapon(random.randint(2, 4), "Rare")
                    self.add_item(weapon)
                elif item_type == "armor":
                    armor = ItemFactory.create_random_armor(random.randint(2, 4), "Rare")
                    self.add_item(armor)
    
    def display(self) -> str:
        """Get a string representation of the shop"""
        result = f"{self.name} ({self.shop_type} Shop)\n"
        result += f"Available Gold: {self.gold}\n\n"
        
        if not self.items:
            result += "This shop has no items for sale."
            return result
        
        result += "Items for sale:\n"
        
        # Group items by type
        items_by_type = {}
        for item in self.items:
            if item.type not in items_by_type:
                items_by_type[item.type] = []
            items_by_type[item.type].append(item)
        
        # Display items by type
        for item_type, items in items_by_type.items():
            result += f"\n{item_type}s:\n"
            for i, item in enumerate(items, 1):
                price = self.get_buy_price(item)
                if item.quantity > 1:
                    result += f"{i}. {item.name} (x{item.quantity}) - {price} gold each\n"
                else:
                    result += f"{i}. {item.name} - {price} gold\n"
        
        return result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert shop to dictionary for saving"""
        return {
            "name": self.name,
            "shop_type": self.shop_type,
            "items": [item.to_dict() for item in self.items],
            "buy_multiplier": self.buy_multiplier,
            "sell_multiplier": self.sell_multiplier,
            "gold": self.gold,
            "restock_time": self.restock_time,
            "specialty_items": self.specialty_items
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Shop':
        """Create shop from dictionary data"""
        shop = cls(data["name"], data["shop_type"])
        shop.buy_multiplier = data["buy_multiplier"]
        shop.sell_multiplier = data["sell_multiplier"]
        shop.gold = data["gold"]
        shop.restock_time = data["restock_time"]
        shop.specialty_items = data["specialty_items"]
        
        # Add items to shop
        for item_data in data["items"]:
            item = ItemFactory.create_item(item_data)
            shop.items.append(item)
        
        return shop


# Example usage of the items and inventory module (for testing)
if __name__ == "__main__":
    # Create some items
    sword = Weapon("Iron Sword", "A basic iron sword.", 25, 8)
    sword.weapon_type = "Sword"
    
    armor = Armor("Leather Armor", "Basic leather armor.", 30, 5)
    armor.armor_type = "Light"
    armor.equip_slot = "Body"
    
    potion = Potion("Health Potion", "Restores health when consumed.", 15, 30)
    potion.effect_type = "Health"
    potion.quantity = 3
    
    # Create a player inventory
    inventory = Inventory()
    
    # Add items to inventory
    inventory.add_item(sword)
    inventory.add_item(armor)
    inventory.add_item(potion)
    
    # Display inventory
    print(inventory.display())
    
    # Equip items
    print("\nEquipping items...")
    inventory.equip_item(sword.unique_id)
    inventory.equip_item(armor.unique_id)
    
    # Display equipped items
    print(inventory.display_equipped())
    
    # Display updated inventory
    print(inventory.display())
    
    # Create a shop
    print("\nCreating shop...")
    shop = Shop("Adventurer's Supply", "General")
    shop.restock()
    
    # Display shop
    print(shop.display())
    
    # Create a random weapon using ItemFactory
    print("\nCreating random weapon...")
    random_weapon = ItemFactory.create_random_weapon(level=3)
    print(random_weapon.get_full_description())
    
    # Create a random armor using ItemFactory
    print("\nCreating random armor...")
    random_armor = ItemFactory.create_random_armor(level=3)
    print(random_armor.get_full_description())
    
    # Create a random potion using ItemFactory
    print("\nCreating random potion...")
    random_potion = ItemFactory.create_random_potion(level=2)
    print(random_potion.get_full_description())
