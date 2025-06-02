#!/usr/bin/env python3
"""
Adventure Quest - Text-Based Multiplayer Adventure Game
Combat System Module
Contributed by: Hemanth
"""

import random
import time
import json
from typing import Dict, List, Optional, Any, Union, Tuple


class Enemy:
    """Class representing an enemy in the game"""
    def __init__(self, name: str, level: int = 1):
        self.name = name
        self.level = level
        self.max_health = 20 + (level * 10)
        self.health = self.max_health
        self.attack = 5 + (level * 2)
        self.defense = 2 + level
        self.experience_reward = 20 + (level * 15)
        self.gold_reward = 5 + (level * 3)
        self.item_drop_chance = 0.3  # 30% chance to drop an item
        self.possible_drops = []
        self.attack_messages = [
            "swings at you with great force",
            "lunges toward you",
            "attacks with a fierce growl",
            "strikes quickly"
        ]
        self.enemy_type = "Normal"  # Normal, Elite, Boss
        self.abilities = {}  # Special abilities
        self.resistances = {}  # Damage resistances by type
        self.weaknesses = {}  # Damage weaknesses by type
        self.description = f"A level {level} {name}."
    
    def take_damage(self, amount: int) -> int:
        """
        Reduce enemy health by damage amount after defense calculations
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
    
    def is_alive(self) -> bool:
        """Check if enemy is alive"""
        return self.health > 0
    
    def attack_player(self, player: Any) -> Tuple[int, str]:
        """
        Attack a player
        Returns (damage_dealt, message)
        """
        # Calculate damage
        damage = self.attack
        
        # Apply random variation (±20%)
        variation = random.uniform(0.8, 1.2)
        damage = int(damage * variation)
        
        # Get a random attack message
        message = random.choice(self.attack_messages)
        
        # Have player take damage
        actual_damage = player.take_damage(damage)
        
        return actual_damage, f"The {self.name} {message} and deals {actual_damage} damage."
    
    def use_ability(self, player: Any) -> Tuple[int, str]:
        """
        Use a special ability on a player
        Returns (damage_or_effect, message)
        """
        if not self.abilities:
            return self.attack_player(player)
        
        # 30% chance to use a special ability if available
        if random.random() < 0.3 and self.abilities:
            ability_name = random.choice(list(self.abilities.keys()))
            ability = self.abilities[ability_name]
            
            if ability["type"] == "damage":
                # Damage ability
                damage = int(self.attack * ability["multiplier"])
                actual_damage = player.take_damage(damage)
                return actual_damage, f"The {self.name} uses {ability_name} and deals {actual_damage} damage!"
                
            elif ability["type"] == "heal":
                # Healing ability
                heal_amount = int(self.max_health * ability["multiplier"])
                before_heal = self.health
                self.health += heal_amount
                if self.health > self.max_health:
                    self.health = self.max_health
                actual_heal = self.health - before_heal
                return actual_heal, f"The {self.name} uses {ability_name} and heals for {actual_heal} health!"
                
            elif ability["type"] == "stun":
                # Stun ability (in a real implementation, this would set a stun flag on the player)
                message = f"The {self.name} uses {ability_name}! You are stunned and lose your next turn!"
                return 0, message
        
        # Default to regular attack if no ability was used
        return self.attack_player(player)
    
    def add_ability(self, name: str, ability_type: str, multiplier: float, chance: float = 0.3) -> None:
        """Add a special ability to the enemy"""
        self.abilities[name] = {
            "type": ability_type,
            "multiplier": multiplier,
            "chance": chance
        }
    
    def add_drop(self, item_data: Dict[str, Any], drop_chance: float = 0.5) -> None:
        """Add a possible item drop with its chance"""
        self.possible_drops.append({
            "item": item_data,
            "chance": drop_chance
        })
    
    def get_drops(self) -> List[Dict[str, Any]]:
        """
        Generate drops based on drop chances
        Returns a list of item data dictionaries
        """
        drops = []
        
        # Check for each possible drop
        for drop in self.possible_drops:
            if random.random() < drop["chance"]:
                drops.append(drop["item"])
        
        return drops
    
    def set_enemy_type(self, enemy_type: str) -> None:
        """Set the enemy type and adjust stats accordingly"""
        valid_types = ["Normal", "Elite", "Boss"]
        if enemy_type not in valid_types:
            return
            
        self.enemy_type = enemy_type
        
        # Adjust stats based on enemy type
        if enemy_type == "Elite":
            self.max_health = int(self.max_health * 1.5)
            self.health = self.max_health
            self.attack = int(self.attack * 1.3)
            self.defense = int(self.defense * 1.3)
            self.experience_reward = int(self.experience_reward * 2)
            self.gold_reward = int(self.gold_reward * 2)
            self.item_drop_chance = 0.6  # 60% chance to drop an item
            
        elif enemy_type == "Boss":
            self.max_health = self.max_health * 3
            self.health = self.max_health
            self.attack = int(self.attack * 2)
            self.defense = int(self.defense * 1.5)
            self.experience_reward = self.experience_reward * 5
            self.gold_reward = self.gold_reward * 5
            self.item_drop_chance = 1.0  # 100% chance to drop an item
    
    def add_resistance(self, damage_type: str, percentage: float) -> None:
        """Add a damage resistance (percentage as decimal, e.g., 0.5 for 50%)"""
        self.resistances[damage_type] = percentage
    
    def add_weakness(self, damage_type: str, percentage: float) -> None:
        """Add a damage weakness (percentage as decimal, e.g., 0.5 for 50% more damage)"""
        self.weaknesses[damage_type] = percentage
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert enemy to dictionary for saving"""
        return {
            "name": self.name,
            "level": self.level,
            "max_health": self.max_health,
            "health": self.health,
            "attack": self.attack,
            "defense": self.defense,
            "experience_reward": self.experience_reward,
            "gold_reward": self.gold_reward,
            "item_drop_chance": self.item_drop_chance,
            "possible_drops": self.possible_drops,
            "attack_messages": self.attack_messages,
            "enemy_type": self.enemy_type,
            "abilities": self.abilities,
            "resistances": self.resistances,
            "weaknesses": self.weaknesses,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Enemy':
        """Create enemy from dictionary data"""
        enemy = cls(data["name"], data["level"])
        enemy.max_health = data["max_health"]
        enemy.health = data["health"]
        enemy.attack = data["attack"]
        enemy.defense = data["defense"]
        enemy.experience_reward = data["experience_reward"]
        enemy.gold_reward = data["gold_reward"]
        enemy.item_drop_chance = data["item_drop_chance"]
        enemy.possible_drops = data["possible_drops"]
        enemy.attack_messages = data["attack_messages"]
        enemy.enemy_type = data["enemy_type"]
        enemy.abilities = data["abilities"]
        enemy.resistances = data["resistances"]
        enemy.weaknesses = data["weaknesses"]
        enemy.description = data["description"]
        return enemy


class EnemyFactory:
    """Factory class for creating different types of enemies"""
    
    @staticmethod
    def create_enemy(name: str, level: int) -> Enemy:
        """Create a basic enemy with given name and level"""
        return Enemy(name, level)
    
    @staticmethod
    def create_enemy_from_template(template: str, level: int) -> Enemy:
        """Create an enemy based on a predefined template"""
        if template == "Wolf":
            enemy = Enemy("Wolf", level)
            enemy.attack = 6 + (level * 2)
            enemy.defense = 3 + level
            enemy.description = "A fierce wolf with sharp teeth and quick movements."
            enemy.attack_messages = [
                "lunges at you with sharp teeth",
                "claws at you viciously",
                "bites at your leg",
                "howls and charges at you"
            ]
            
            # Add possible drops
            enemy.add_drop({"name": "Wolf Pelt", "type": "Material", "value": 5 + level}, 0.7)
            enemy.add_drop({"name": "Wolf Fang", "type": "Material", "value": 8 + (level * 2)}, 0.4)
            
            return enemy
            
        elif template == "Goblin":
            enemy = Enemy("Goblin", level)
            enemy.attack = 5 + (level * 2)
            enemy.defense = 2 + level
            enemy.description = "A small, green-skinned creature with a mischievous grin."
            enemy.attack_messages = [
                "swings a crude dagger at you",
                "throws a small rock at your head",
                "stabs at you with a sharpened stick",
                "jumps at you with its claws out"
            ]
            
            # Add ability
            enemy.add_ability("Sneak Attack", "damage", 1.5, 0.2)
            
            # Add possible drops
            enemy.add_drop({"name": "Goblin Ear", "type": "Material", "value": 3 + level}, 0.6)
            enemy.add_drop({"name": "Crude Dagger", "type": "Weapon", "damage": 4 + level, "value": 10 + (level * 3)}, 0.3)
            
            return enemy
            
        elif template == "Skeleton":
            enemy = Enemy("Skeleton", level)
            enemy.attack = 7 + (level * 2)
            enemy.defense = 4 + level
            enemy.description = "An animated skeleton, its bones clacking as it moves."
            enemy.attack_messages = [
                "swings a rusty sword at you",
                "tries to grab you with bony fingers",
                "thrusts a broken blade toward you",
                "attacks with an eerie silence"
            ]
            
            # Add resistances and weaknesses
            enemy.add_resistance("pierce", 0.3)  # 30% resistance to piercing damage
            enemy.add_weakness("crush", 0.5)  # 50% weakness to crushing damage
            
            # Add possible drops
            enemy.add_drop({"name": "Bone Shard", "type": "Material", "value": 4 + level}, 0.8)
            enemy.add_drop({"name": "Rusty Sword", "type": "Weapon", "damage": 5 + level, "value": 8 + (level * 2)}, 0.4)
            
            return enemy
            
        elif template == "Troll":
            enemy = Enemy("Troll", level)
            enemy.max_health = 40 + (level * 15)
            enemy.health = enemy.max_health
            enemy.attack = 10 + (level * 3)
            enemy.defense = 6 + (level * 2)
            enemy.experience_reward = 35 + (level * 20)
            enemy.gold_reward = 15 + (level * 5)
            enemy.description = "A large, muscular troll with tough skin and a nasty temperament."
            enemy.attack_messages = [
                "smashes its club down at you",
                "swings a massive fist toward your head",
                "tries to grab and crush you",
                "roars and charges at you"
            ]
            
            # Add ability
            enemy.add_ability("Regenerate", "heal", 0.1, 0.4)
            
            # Add possible drops
            enemy.add_drop({"name": "Troll Hide", "type": "Material", "value": 20 + (level * 5)}, 0.6)
            enemy.add_drop({"name": "Troll Club", "type": "Weapon", "damage": 12 + (level * 3), "value": 25 + (level * 8)}, 0.3)
            
            return enemy
            
        elif template == "Dragon":
            enemy = Enemy("Dragon", level)
            enemy.set_enemy_type("Boss")
            enemy.description = "A massive dragon with scales like armor and fiery breath."
            enemy.attack_messages = [
                "breathes a torrent of fire at you",
                "slashes with razor-sharp claws",
                "whips its spiked tail toward you",
                "snaps at you with massive jaws"
            ]
            
            # Add abilities
            enemy.add_ability("Fire Breath", "damage", 2.0, 0.4)
            enemy.add_ability("Wing Buffet", "stun", 0, 0.2)
            
            # Add resistances
            enemy.add_resistance("fire", 0.8)  # 80% resistance to fire damage
            
            # Add possible drops (guaranteed for boss)
            enemy.add_drop({"name": "Dragon Scale", "type": "Material", "value": 100 + (level * 20)}, 1.0)
            enemy.add_drop({"name": "Dragon Tooth", "type": "Material", "value": 80 + (level * 15)}, 0.8)
            enemy.add_drop({"name": "Dragon Fire Essence", "type": "Material", "value": 150 + (level * 25)}, 0.5)
            
            return enemy
        
        # Default to a basic enemy if template not found
        return Enemy(name, level)
    
    @staticmethod
    def create_random_enemy(level: int, location_type: str = "Any") -> Enemy:
        """Create a random enemy appropriate for a given level and location"""
        # Define enemy templates by location type
        enemy_templates = {
            "Forest": ["Wolf", "Goblin", "Bear"],
            "Cave": ["Bat", "Skeleton", "Troll"],
            "Mountain": ["Wolf", "Eagle", "Yeti"],
            "Swamp": ["Alligator", "Poison Spider", "Slime"],
            "Desert": ["Scorpion", "Sand Worm", "Mummy"],
            "Ruins": ["Skeleton", "Ghost", "Animated Armor"],
            "Any": ["Wolf", "Goblin", "Skeleton", "Bandit", "Slime"]
        }
        
        # Select template based on location
        templates = enemy_templates.get(location_type, enemy_templates["Any"])
        template = random.choice(templates)
        
        # Create base enemy
        enemy = Enemy(template, level)
        
        # Customize based on template
        if template == "Wolf":
            enemy.attack_messages = [
                "lunges at you with sharp teeth",
                "claws at you viciously",
                "bites at your leg",
                "howls and charges at you"
            ]
            enemy.add_drop({"name": "Wolf Pelt", "type": "Material", "value": 5 + level}, 0.7)
            
        elif template == "Goblin":
            enemy.description = "A small, green-skinned creature with a mischievous grin."
            enemy.attack_messages = [
                "swings a crude dagger at you",
                "throws a small rock at your head",
                "stabs at you with a sharpened stick",
                "jumps at you with its claws out"
            ]
            enemy.add_ability("Sneak Attack", "damage", 1.5, 0.2)
            
        elif template == "Skeleton":
            enemy.description = "An animated skeleton, its bones clacking as it moves."
            enemy.add_resistance("pierce", 0.3)
            enemy.add_weakness("crush", 0.5)
            
        elif template == "Bandit":
            enemy.description = "A rough-looking human wielding a weapon and looking for trouble."
            enemy.add_ability("Disarm", "stun", 0, 0.2)
            enemy.add_drop({"name": "Stolen Goods", "type": "Miscellaneous", "value": 10 + (level * 3)}, 0.6)
            
        elif template == "Slime":
            enemy.description = "A gelatinous blob that oozes across the ground."
            enemy.attack = 4 + (level * 2)
            enemy.defense = 2 + level
            enemy.add_resistance("pierce", 0.5)
            enemy.add_weakness("fire", 0.3)
            enemy.attack_messages = [
                "engulfs your foot",
                "sprays acidic goo at you",
                "stretches and slams into you",
                "attempts to absorb your weapon"
            ]
        
        # Random chance for an elite enemy
        if random.random() < 0.1:  # 10% chance
            enemy.set_enemy_type("Elite")
            enemy.name = f"Elite {enemy.name}"
        
        return enemy


class Combat:
    """Class for handling combat encounters"""
    def __init__(self):
        self.players = []
        self.enemies = []
        self.turn_order = []
        self.current_turn = 0
        self.round_number = 1
        self.is_active = False
        self.combat_log = []
        self.initiative_order = []
    
    def add_player(self, player: Any) -> None:
        """Add a player to the combat"""
        self.players.append(player)
    
    def add_enemy(self, enemy: Enemy) -> None:
        """Add an enemy to the combat"""
        self.enemies.append(enemy)
    
    def start_combat(self) -> str:
        """Start a combat encounter and determine initiative order"""
        if not self.players or not self.enemies:
            return "Cannot start combat without both players and enemies."
        
        self.is_active = True
        self.round_number = 1
        self.combat_log = []
        
        # Determine initiative order (simplified version)
        all_combatants = []
        
        # Add players with their initiative
        for player in self.players:
            initiative = random.randint(1, 20)
            if hasattr(player, 'speed'):
                initiative += player.speed
            all_combatants.append({"type": "player", "entity": player, "initiative": initiative})
        
        # Add enemies with their initiative
        for enemy in self.enemies:
            initiative = random.randint(1, 20)
            all_combatants.append({"type": "enemy", "entity": enemy, "initiative": initiative})
        
        # Sort by initiative (higher goes first)
        all_combatants.sort(key=lambda x: x["initiative"], reverse=True)
        
        # Set the turn order
        self.initiative_order = all_combatants
        self.turn_order = all_combatants.copy()
        self.current_turn = 0
        
        # Log the combat start
        start_message = "Combat has begun!\n"
        start_message += "Initiative order:\n"
        
        for i, combatant in enumerate(self.initiative_order, 1):
            entity = combatant["entity"]
            if combatant["type"] == "player":
                start_message += f"{i}. {entity.name} (Player) - Initiative: {combatant['initiative']}\n"
            else:
                start_message += f"{i}. {entity.name} (Enemy) - Initiative: {combatant['initiative']}\n"
        
        self.add_to_log(start_message)
        return start_message
    
    def next_turn(self) -> Tuple[bool, str]:
        """
        Process the next turn in combat
        Returns (is_combat_over, message)
        """
        if not self.is_active:
            return True, "Combat is not active."
        
        # Check if combat should end
        if self.check_combat_end():
            return True, self.end_combat()
        
        # Get the current combatant
        current = self.turn_order[self.current_turn]
        entity = current["entity"]
        
        message = ""
        
        if current["type"] == "enemy":
            # Enemy's turn
            if entity.is_alive():
                # Pick a random player target
                alive_players = [p for p in self.players if p.is_alive()]
                if alive_players:
                    target = random.choice(alive_players)
                    
                    # Decide whether to use an ability or regular attack
                    if entity.abilities and random.random() < 0.3:
                        damage, attack_msg = entity.use_ability(target)
                    else:
                        damage, attack_msg = entity.attack_player(target)
                    
                    message = f"{entity.name}'s turn: {attack_msg}"
                    
                    # Check if target was defeated
                    if not target.is_alive():
                        message += f"\n{target.name} has been defeated!"
                else:
                    message = f"{entity.name}'s turn: There are no targets available."
            else:
                message = f"{entity.name}'s turn: But it's already defeated."
        
        # Advance to the next turn
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        
        # If we've gone through everyone, start a new round
        if self.current_turn == 0:
            self.round_number += 1
            message += f"\nRound {self.round_number} begins!"
            
            # Rebuild the turn order in case any combatants were defeated
            self.rebuild_turn_order()
        
        self.add_to_log(message)
        return self.check_combat_end(), message
    
    def player_action(self, player: Any, action: str, target_index: int = 0, skill_name: str = None) -> Tuple[bool, str]:
        """
        Process a player's action during their turn
        Returns (is_combat_over, message)
        """
        if not self.is_active:
            return True, "Combat is not active."
        
        # Check if it's this player's turn
        current = self.turn_order[self.current_turn]
        if current["type"] != "player" or current["entity"] != player:
            return False, "It's not your turn yet."
        
        message = ""
        
        # Get the target enemy
        if 0 <= target_index < len(self.enemies):
            target = self.enemies[target_index]
            
            if action == "attack":
                # Basic attack
                attack_value = player.attack
                if hasattr(player, 'equipped_items') and player.equipped_items.get("Weapon"):
                    weapon = player.equipped_items["Weapon"]
                    if hasattr(weapon, 'get_damage'):
                        attack_value = weapon.get_damage()
                
                # Apply random variation (±20%)
                variation = random.uniform(0.8, 1.2)
                damage = int(attack_value * variation)
                
                # Apply damage to enemy
                actual_damage = target.take_damage(damage)
                
                message = f"{player.name}'s turn: You attack the {target.name} for {actual_damage} damage!"
                
                # Check if enemy was defeated
                if not target.is_alive():
                    xp_reward = target.experience_reward
                    gold_reward = target.gold_reward
                    
                    # Award XP to the player
                    level_up = False
                    if hasattr(player, 'gain_experience'):
                        level_up = player.gain_experience(xp_reward)
                    
                    # Award gold to the player
                    if hasattr(player, 'gold'):
                        player.gold += gold_reward
                    
                    message += f"\nYou defeated the {target.name}!"
                    message += f"\nYou gained {xp_reward} experience and {gold_reward} gold!"
                    
                    if level_up:
                        message += f"\nCongratulations! You leveled up to level {player.level}!"
                    
                    # Check for item drops
                    if random.random() < target.item_drop_chance:
                        drops = target.get_drops()
                        if drops and hasattr(player, 'add_to_inventory'):
                            for item in drops:
                                player.add_to_inventory(item)
                                message += f"\nThe {target.name} dropped {item['name']}!"
            
            elif action == "skill" and skill_name:
                # Use a skill
                if not hasattr(player, 'skills') or skill_name not in player.skills:
                    message = f"{player.name}'s turn: You don't have the skill {skill_name}."
                else:
                    skill = player.skills[skill_name]
                    mana_cost = skill.get("mana_cost", 0)
                    
                    # Check if player has enough mana
                    if hasattr(player, 'mana') and player.mana < mana_cost:
                        message = f"{player.name}'s turn: You don't have enough mana to use {skill_name}."
                    else:
                        # Use mana
                        if hasattr(player, 'use_mana'):
                            player.use_mana(mana_cost)
                        
                        # Calculate damage
                        base_damage = player.attack
                        if hasattr(player, 'equipped_items') and player.equipped_items.get("Weapon"):
                            weapon = player.equipped_items["Weapon"]
                            if hasattr(weapon, 'get_damage'):
                                base_damage = weapon.get_damage()
                        
                        damage = int(base_damage * skill.get("damage_multiplier", 1.0))
                        
                        # Apply damage to enemy
                        actual_damage = target.take_damage(damage)
                        
                        message = f"{player.name}'s turn: You use {skill_name} on the {target.name} for {actual_damage} damage!"
                        
                        # Check if enemy was defeated
                        if not target.is_alive():
                            xp_reward = target.experience_reward
                            gold_reward = target.gold_reward
                            
                            # Award XP to the player
                            level_up = False
                            if hasattr(player, 'gain_experience'):
                                level_up = player.gain_experience(xp_reward)
                            
                            # Award gold to the player
                            if hasattr(player, 'gold'):
                                player.gold += gold_reward
                            
                            message += f"\nYou defeated the {target.name}!"
                            message += f"\nYou gained {xp_reward} experience and {gold_reward} gold!"
                            
                            if level_up:
                                message += f"\nCongratulations! You leveled up to level {player.level}!"
                            
                            # Check for item drops
                            if random.random() < target.item_drop_chance:
                                drops = target.get_drops()
                                if drops and hasattr(player, 'add_to_inventory'):
                                    for item in drops:
                                        player.add_to_inventory(item)
                                        message += f"\nThe {target.name} dropped {item['name']}!"
            
            elif action == "item":
                # Using an item would be handled here
                message = f"{player.name}'s turn: Item usage is not implemented yet."
            
            elif action == "flee":
                # Attempt to flee combat
                flee_chance = 0.5  # 50% base chance to flee
                
                # Adjust based on player vs enemy levels
                player_level = getattr(player, 'level', 1)
                enemy_levels = sum(e.level for e in self.enemies)
                level_diff = player_level - (enemy_levels / len(self.enemies))
                
                flee_chance += level_diff * 0.05  # +5% per level difference
                
                if random.random() < flee_chance:
                    self.is_active = False
                    message = f"{player.name}'s turn: You successfully fled from combat!"
                    return True, message
                else:
                    message = f"{player.name}'s turn: You tried to flee but couldn't escape!"
            
            else:
                message = f"{player.name}'s turn: Invalid action."
        else:
            message = f"{player.name}'s turn: Invalid target."
        
        # Advance to the next turn
        self.current_turn = (self.current_turn + 1) % len(self.turn_order)
        
        # If we've gone through everyone, start a new round
        if self.current_turn == 0:
            self.round_number += 1
            message += f"\nRound {self.round_number} begins!"
            
            # Rebuild the turn order in case any combatants were defeated
            self.rebuild_turn_order()
        
        self.add_to_log(message)
        return self.check_combat_end(), message
    
    def rebuild_turn_order(self) -> None:
        """Rebuild the turn order based on who's still alive"""
        # Keep the same initiative order but remove defeated combatants
        self.turn_order = []
        
        for combatant in self.initiative_order:
            entity = combatant["entity"]
            if (combatant["type"] == "player" and entity.is_alive()) or \
               (combatant["type"] == "enemy" and entity.is_alive()):
                self.turn_order.append(combatant)
        
        # Reset turn index if needed
        if self.current_turn >= len(self.turn_order):
            self.current_turn = 0
    
    def check_combat_end(self) -> bool:
        """Check if combat should end"""
        # Combat ends if all players or all enemies are defeated
        players_alive = any(player.is_alive() for player in self.players)
        enemies_alive = any(enemy.is_alive() for enemy in self.enemies)
        
        return not (players_alive and enemies_alive) or not self.is_active
    
    def end_combat(self) -> str:
        """End combat and determine results"""
        if not self.is_active:
            return "Combat already ended."
        
        self.is_active = False
        
        # Determine outcome
        players_alive = any(player.is_alive() for player in self.players)
        
        message = "Combat has ended.\n"
        
        if players_alive:
            message += "Victory! All enemies have been defeated."
        else:
            message += "Defeat! All players have been defeated."
        
        self.add_to_log(message)
        return message
    
    def get_combat_state(self) -> str:
        """Get a string representation of the current combat state"""
        if not self.is_active:
            return "No active combat."
        
        state = f"=== Combat Round {self.round_number} ===\n"
        
        # Display players
        state += "\nPlayers:\n"
        for player in self.players:
            health_status = f"{player.health}/{player.max_health} HP"
            if hasattr(player, 'mana'):
                health_status += f", {player.mana}/{player.max_mana} MP"
            
            status = "Alive" if player.is_alive() else "Defeated"
            state += f"{player.name}: {health_status} - {status}\n"
        
        # Display enemies
        state += "\nEnemies:\n"
        for i, enemy in enumerate(self.enemies, 1):
            health_status = f"{enemy.health}/{enemy.max_health} HP"
            status = "Alive" if enemy.is_alive() else "Defeated"
            state += f"{i}. {enemy.name}: {health_status} - {status}\n"
        
        # Display whose turn it is
        if 0 <= self.current_turn < len(self.turn_order):
            current = self.turn_order[self.current_turn]
            entity = current["entity"]
            turn_type = "player" if current["type"] == "player" else "enemy"
            state += f"\nCurrent turn: {entity.name} ({turn_type})"
        
        return state
    
    def add_to_log(self, message: str) -> None:
        """Add a message to the combat log"""
        timestamp = time.strftime("%H:%M:%S")
        self.combat_log.append(f"[{timestamp}] {message}")
    
    def get_combat_log(self) -> str:
        """Get the combat log as a string"""
        return "\n".join(self.combat_log)


class CombatSystem:
    """Main class for managing combat in the game"""
    def __init__(self):
        self.active_combats = {}
        self.encounter_templates = {}
        self.global_drop_tables = {}
    
    def create_combat(self, players: List[Any], enemies: List[Enemy]) -> str:
        """Create a new combat instance with given players and enemies"""
        combat_id = f"combat_{int(time.time())}"
        
        combat = Combat()
        
        # Add players
        for player in players:
            combat.add_player(player)
        
        # Add enemies
        for enemy in enemies:
            combat.add_enemy(enemy)
        
        # Start combat
        start_message = combat.start_combat()
        
        # Store the combat
        self.active_combats[combat_id] = combat
        
        return f"Combat created with ID: {combat_id}\n{start_message}"
    
    def end_combat(self, combat_id: str) -> str:
        """End a combat by ID"""
        if combat_id in self.active_combats:
            combat = self.active_combats[combat_id]
            result = combat.end_combat()
            del self.active_combats[combat_id]
            return result
        else:
            return f"No combat found with ID: {combat_id}"
    
    def get_combat(self, combat_id: str) -> Optional[Combat]:
        """Get a combat instance by ID"""
        return self.active_combats.get(combat_id)
    
    def add_encounter_template(self, name: str, enemies: List[Dict[str, Any]], min_level: int = 1) -> None:
        """Add a predefined encounter template"""
        self.encounter_templates[name] = {
            "enemies": enemies,
            "min_level": min_level
        }
    
    def create_encounter_from_template(self, template_name: str, player_level: int) -> List[Enemy]:
        """Create enemies from a template, scaling to player level"""
        if template_name not in self.encounter_templates:
            return []
        
        template = self.encounter_templates[template_name]
        
        # Scale enemies based on player level
        enemies = []
        for enemy_data in template["enemies"]:
            # Determine enemy level based on player level and template min level
            level_diff = player_level - template["min_level"]
            enemy_level = max(1, enemy_data.get("level", 1) + level_diff)
            
            # Create the enemy
            enemy_name = enemy_data.get("name", "Unknown")
            enemy_template = enemy_data.get("template")
            
            if enemy_template:
                enemy = EnemyFactory.create_enemy_from_template(enemy_template, enemy_level)
            else:
                enemy = Enemy(enemy_name, enemy_level)
            
            # Set enemy type if specified
            enemy_type = enemy_data.get("type")
            if enemy_type:
                enemy.set_enemy_type(enemy_type)
            
            enemies.append(enemy)
        
        return enemies
    
    def create_random_encounter(self, location_type: str, player_level: int, num_enemies: int = 1) -> List[Enemy]:
        """Create a random encounter appropriate for location and player level"""
        enemies = []
        
        for _ in range(num_enemies):
            # Adjust enemy level slightly from player level
            level_adjustment = random.choice([-1, -1, 0, 0, 0, 1, 1])
            enemy_level = max(1, player_level + level_adjustment)
            
            # Create enemy based on location
            enemy = EnemyFactory.create_random_enemy(enemy_level, location_type)
            enemies.append(enemy)
        
        # Small chance for an elite enemy if multiple enemies
        if num_enemies > 1 and random.random() < 0.2:  # 20% chance
            strongest_enemy = max(enemies, key=lambda e: e.level)
            strongest_enemy.set_enemy_type("Elite")
            strongest_enemy.name = f"Elite {strongest_enemy.name}"
        
        return enemies
    
    def add_drop_table(self, name: str, items: List[Dict[str, Any]]) -> None:
        """Add a global drop table for enemies"""
        self.global_drop_tables[name] = items
    
    def get_drops_from_table(self, table_name: str) -> List[Dict[str, Any]]:
        """Get random drops from a named drop table"""
        if table_name not in self.global_drop_tables:
            return []
        
        drops = []
        for item in self.global_drop_tables[table_name]:
            chance = item.get("chance", 1.0)
            if random.random() < chance:
                # Create a copy of the item without the chance property
                item_copy = item.copy()
                if "chance" in item_copy:
                    del item_copy["chance"]
                drops.append(item_copy)
        
        return drops


# Example usage of the combat system (for testing)
if __name__ == "__main__":
    # Create a mock player for testing
    class MockPlayer:
        def __init__(self, name, level=1):
            self.name = name
            self.level = level
            self.max_health = 100
            self.health = 100
            self.attack = 10
            self.defense = 5
            self.gold = 50
            self.inventory = []
        
        def is_alive(self):
            return self.health > 0
        
        def take_damage(self, amount):
            actual_damage = max(1, amount - self.defense)
            self.health -= actual_damage
            if self.health < 0:
                self.health = 0
            return actual_damage
        
        def gain_experience(self, amount):
            print(f"{self.name} gained {amount} experience!")
            return False
        
        def add_to_inventory(self, item):
            self.inventory.append(item)
            print(f"{self.name} added {item['name']} to inventory!")
    
    # Create a test player
    player = MockPlayer("TestPlayer", 3)
    
    # Create a test enemy
    goblin = EnemyFactory.create_enemy_from_template("Goblin", 2)
    wolf = Enemy("Wolf", 1)
    
    # Create a combat instance
    combat = Combat()
    combat.add_player(player)
    combat.add_enemy(goblin)
    combat.add_enemy(wolf)
    
    # Start combat
    print(combat.start_combat())
    
    # Display combat state
    print("\n" + combat.get_combat_state())
    
    # Simulate some turns
    while not combat.check_combat_end():
        current = combat.turn_order[combat.current_turn]
        
        if current["type"] == "player":
            # Player's turn
            is_over, message = combat.player_action(player, "attack", 0)
            print("\n" + message)
        else:
            # Enemy's turn
            is_over, message = combat.next_turn()
            print("\n" + message)
        
        print("\n" + combat.get_combat_state())
        
        if is_over:
            break
    
    # End combat
    print("\n" + combat.end_combat())
    
    # Display combat log
    print("\nCombat Log:")
    print(combat.get_combat_log()
