:#!/usr/bin/env python3
"""
Adventure Quest - Text-Based Multiplayer Adventure Game
Player Module
Contributed by: Mohammed Irfan
"""

import json
import os
import time
import random
from typing import Dict, List, Optional, Any, Union


class Player:
    """Player class representing a character in the game"""
    def __init__(self, name: str, player_class: str):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.experience = 0
        self.location = "Town Square"
        
        # Base stats initialization
        self.max_health = 100
        self.health = 100
        self.mana = 50
        self.max_mana = 50
        self.attack = 10
        self.defense = 5
        self.speed = 5
        
        # Inventory initialization (will be managed by items_inventory.py)
        self.inventory = []
        self.gold = 50
        self.equipment = {
            "weapon": None,
            "armor": None,
            "accessory": None
        }
        
        # Class-specific stat adjustments
        self._apply_class_bonuses()
        
        # Skills available to the player
        self.skills = self._get_class_skills()
        
        # Quest tracking
        self.active_quests = []
        self.completed_quests = []
        
        # Friendship levels with NPCs
        self.relationships = {}
        
    def _apply_class_bonuses(self) -> None:
        """Apply stat bonuses based on player class"""
        if self.player_class == "Warrior":
            self.max_health += 20
            self.health += 20
            self.attack += 5
            self.defense += 3
            self.mana -= 20
            self.max_mana -= 20
        elif self.player_class == "Mage":
            self.max_mana += 30
            self.mana += 30
            self.attack += 2
            self.defense -= 1
        elif self.player_class == "Rogue":
            self.speed += 5
            self.attack += 3
            self.defense -= 1
        elif self.player_class == "Cleric":
            self.max_health += 10
            self.health += 10
            self.max_mana += 20
            self.mana += 20
            self.defense += 1
    
    def _get_class_skills(self) -> Dict[str, Dict[str, Any]]:
        """Get skills available to the player based on their class"""
        base_skills = {
            "Basic Attack": {
                "description": "A basic attack with your equipped weapon",
                "damage_multiplier": 1.0,
                "mana_cost": 0,
                "level_requirement": 1
            }
        }
        
        class_skills = {
            "Warrior": {
                "Heroic Strike": {
                    "description": "A powerful strike that deals extra damage",
                    "damage_multiplier": 1.5,
                    "mana_cost": 10,
                    "level_requirement": 2
                },
                "Whirlwind": {
                    "description": "Spin and hit all enemies around you",
                    "damage_multiplier": 1.2,
                    "mana_cost": 15,
                    "level_requirement": 4
                },
                "Shield Block": {
                    "description": "Block the next attack completely",
                    "damage_multiplier": 0,
                    "mana_cost": 10,
                    "level_requirement": 3
                }
            },
            "Mage": {
                "Fireball": {
                    "description": "Hurl a ball of fire at your enemy",
                    "damage_multiplier": 1.7,
                    "mana_cost": 15,
                    "level_requirement": 2
                },
                "Frost Nova": {
                    "description": "Freeze enemies in place and deal damage",
                    "damage_multiplier": 1.3,
                    "mana_cost": 20,
                    "level_requirement": 3
                },
                "Arcane Missiles": {
                    "description": "Launch multiple arcane projectiles",
                    "damage_multiplier": 2.0,
                    "mana_cost": 25,
                    "level_requirement": 5
                }
            },
            "Rogue": {
                "Backstab": {
                    "description": "Stab the enemy from behind for extra damage",
                    "damage_multiplier": 1.8,
                    "mana_cost": 12,
                    "level_requirement": 2
                },
                "Vanish": {
                    "description": "Become invisible and avoid the next attack",
                    "damage_multiplier": 0,
                    "mana_cost": 18,
                    "level_requirement": 4
                },
                "Poison Strike": {
                    "description": "Poison your weapon for continuous damage",
                    "damage_multiplier": 1.2,
                    "mana_cost": 15,
                    "level_requirement": 3
                }
            },
            "Cleric": {
                "Smite": {
                    "description": "Call down holy light to damage an enemy",
                    "damage_multiplier": 1.5,
                    "mana_cost": 12,
                    "level_requirement": 2
                },
                "Heal": {
                    "description": "Restore health to yourself or an ally",
                    "damage_multiplier": 0,
                    "mana_cost": 20,
                    "level_requirement": 1
                },
                "Holy Shield": {
                    "description": "Create a shield that absorbs damage",
                    "damage_multiplier": 0,
                    "mana_cost": 15,
                    "level_requirement": 3
                }
            }
        }
        
        # Add class-specific skills if player level meets requirements
        available_skills = base_skills.copy()
        if self.player_class in class_skills:
            for skill_name, skill_data in class_skills[self.player_class].items():
                if self.level >= skill_data["level_requirement"]:
                    available_skills[skill_name] = skill_data
        
        return available_skills
    
    def gain_experience(self, amount: int) -> bool:
        """
        Add experience points to the player and handle level ups
        Returns True if player leveled up, False otherwise
        """
        self.experience += amount
        
        # Check for level up
        exp_needed_for_next_level = self.level * 100
        if self.experience >= exp_needed_for_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self) -> None:
        """Handle player level up and stat increases"""
        self.level += 1
        
        # Increase stats based on class
        if self.player_class == "Warrior":
            self.max_health += 15
            self.attack += 3
            self.defense += 2
            self.max_mana += 5
        elif self.player_class == "Mage":
            self.max_health += 8
            self.attack += 2
            self.defense += 1
            self.max_mana += 15
        elif self.player_class == "Rogue":
            self.max_health += 10
            self.attack += 4
            self.defense += 1
            self.max_mana += 8
            self.speed += 2
        elif self.player_class == "Cleric":
            self.max_health += 12
            self.attack += 1
            self.defense += 2
            self.max_mana += 12
        
        # Restore health and mana on level up
        self.health = self.max_health
        self.mana = self.max_mana
        
        # Update available skills
        self.skills = self._get_class_skills()
        
        print(f"\nCongratulations! You have reached level {self.level}!")
        print("Your stats have increased!")
        
        # Check for new skills
        new_skills = [skill for skill, data in self.skills.items() 
                     if data["level_requirement"] == self.level]
        
        if new_skills:
            print("You learned new skills:")
            for skill in new_skills:
                print(f"- {skill}: {self.skills[skill]['description']}")
    
    def take_damage(self, amount: int) -> int:
        """
        Reduce player health by damage amount after defense calculations
        Returns the actual damage taken
        """
        # Calculate actual damage based on defense
        defense_multiplier = 100 / (100 + self.defense)
        actual_damage = int(amount * defense_multiplier)
        
        # Ensure minimum damage of 1
        if actual_damage < 1:
            actual_damage = 1
            
        self.health -= actual_damage
        
        # Ensure health doesn't go below 0
        if self.health < 0:
            self.health = 0
            
        return actual_damage
    
    def heal(self, amount: int) -> int:
        """
        Increase player health by heal amount
        Returns the actual amount healed
        """
        before_heal = self.health
        self.health += amount
        
        # Ensure health doesn't exceed max_health
        if self.health > self.max_health:
            self.health = self.max_health
            
        return self.health - before_heal
    
    def use_mana(self, amount: int) -> bool:
        """
        Use mana for skills
        Returns True if player has enough mana, False otherwise
        """
        if self.mana >= amount:
            self.mana -= amount
            return True
        return False
    
    def restore_mana(self, amount: int) -> int:
        """
        Restore player mana
        Returns the actual amount restored
        """
        before_restore = self.mana
        self.mana += amount
        
        # Ensure mana doesn't exceed max_mana
        if self.mana > self.max_mana:
            self.mana = self.max_mana
            
        return self.mana - before_restore
    
    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.health > 0
    
    def add_to_inventory(self, item: Dict[str, Any]) -> bool:
        """
        Add an item to player's inventory
        Returns True if successful, False if inventory is full
        This is a temporary method until items_inventory.py is integrated
        """
        # Simple implementation for now
        self.inventory.append(item)
        return True
    
    def display_stats(self) -> None:
        """Display player stats"""
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Class: {self.player_class}")
        print(f"Level: {self.level}")
        print(f"Experience: {self.experience}/{self.level * 100}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Mana: {self.mana}/{self.max_mana}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Speed: {self.speed}")
        print(f"Gold: {self.gold}")
        print(f"Current Location: {self.location}")
        print("------------------------")
    
    def display_skills(self) -> None:
        """Display player skills"""
        print(f"\n--- {self.name}'s Skills ---")
        for skill_name, skill_data in self.skills.items():
            print(f"{skill_name}: {skill_data['description']}")
            print(f"  Damage Multiplier: {skill_data['damage_multiplier']}")
            print(f"  Mana Cost: {skill_data['mana_cost']}")
            print(f"  Required Level: {skill_data['level_requirement']}")
            print("------------------------")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert player object to dictionary for saving"""
        return {
            "name": self.name,
            "player_class": self.player_class,
            "level": self.level,
            "experience": self.experience,
            "health": self.health,
            "max_health": self.max_health,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "attack": self.attack,
            "defense": self.defense,
            "speed": self.speed,
            "location": self.location,
            "inventory": self.inventory,
            "gold": self.gold,
            "equipment": self.equipment,
            "active_quests": self.active_quests,
            "completed_quests": self.completed_quests,
            "relationships": self.relationships
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Player':
        """Create player object from dictionary data"""
        player = cls(data["name"], data["player_class"])
        player.level = data["level"]
        player.experience = data["experience"]
        player.health = data["health"]
        player.max_health = data["max_health"]
        player.mana = data["mana"]
        player.max_mana = data["max_mana"]
        player.attack = data["attack"]
        player.defense = data["defense"]
        player.speed = data["speed"]
        player.location = data["location"]
        player.inventory = data["inventory"]
        player.gold = data["gold"]
        player.equipment = data["equipment"]
        player.active_quests = data["active_quests"]
        player.completed_quests = data["completed_quests"]
        player.relationships = data["relationships"]
        # Update skills based on level
        player.skills = player._get_class_skills()
        return player


class PlayerManager:
    """Class for managing multiple players in a multiplayer game"""
    def __init__(self):
        self.players = {}
        self.save_file = "players.json"
    
    def add_player(self, player: Player) -> None:
        """Add a player to the manager"""
        self.players[player.name] = player
    
    def remove_player(self, player_name: str) -> bool:
        """Remove a player from the manager"""
        if player_name in self.players:
            del self.players[player_name]
            return True
        return False
    
    def get_player(self, player_name: str) -> Optional[Player]:
        """Get a player by name"""
        return self.players.get(player_name)
    
    def list_players(self) -> List[str]:
        """List all player names"""
        return list(self.players.keys())
    
    def save_players(self) -> bool:
        """Save all players to file"""
        try:
            player_data = {}
            for name, player in self.players.items():
                player_data[name] = player.to_dict()
            
            with open(self.save_file, 'w') as f:
                json.dump(player_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving players: {str(e)}")
            return False
    
    def load_players(self) -> bool:
        """Load players from file"""
        try:
            if not os.path.exists(self.save_file):
                return False
            
            with open(self.save_file, 'r') as f:
                player_data = json.load(f)
            
            self.players = {}
            for name, data in player_data.items():
                self.players[name] = Player.from_dict(data)
            return True
        except Exception as e:
            print(f"Error loading players: {str(e)}")
            return False


# Example usage of the player module (for testing)
if __name__ == "__main__":
    # Create a player manager
    manager = PlayerManager()
    
    # Create a new player
    new_player = Player("TestPlayer", "Warrior")
    
    # Add player to manager
    manager.add_player(new_player)
    
    # Display player stats
    new_player.display_stats()
    
    # Test gaining experience and leveling up
    print("\nGaining experience...")
    new_player.gain_experience(100)  # Should level up to level 2
    
    # Display updated stats
    new_player.display_stats()
    
    # Display skills
    new_player.display_skills()
    
    # Test saving and loading
    print("\nSaving player data...")
    manager.save_players()
    
    print("Creating a new player manager and loading data...")
    new_manager = PlayerManager()
    new_manager.load_players()
    
    # Get the loaded player
    loaded_player = new_manager.get_player("TestPlayer")
    if loaded_player:
        print("Loaded player stats:")
        loaded_player.display_stats()
    else:
        print("Failed to load player.")
