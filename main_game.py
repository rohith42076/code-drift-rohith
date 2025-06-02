#!/usr/bin/env python3
"""
Adventure Quest - Text-Based Multiplayer Adventure Game
Main Game Controller
Contributed by: Rohit Gowda (Team Lead)
"""

import os
import sys
import time
import random
import json
from typing import Dict, List, Tuple, Optional, Any, Union

# These will be imported once teammates contribute their files
# from player_module import Player, PlayerManager
# from game_world import World, Location
# from items_inventory import Item, Inventory
# from combat_system import Combat, Enemy

# Temporary class definitions for testing before teammate contributions
class TempPlayer:
    """Temporary Player class until teammate contributes player_module.py"""
    def _init_(self, name: str, player_class: str):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.max_health = 100
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.inventory = []
        self.experience = 0
        self.location = "Town Square"
    
    def display_stats(self) -> None:
        """Display player stats"""
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Class: {self.player_class}")
        print(f"Level: {self.level}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Experience: {self.experience}")
        print(f"Current Location: {self.location}")
        print("------------------------\n")

class GameManager:
    """Main game controller class"""
    def _init_(self):
        self.players = {}
        self.active_player = None
        self.game_running = True
        self.save_file = "game_save.json"
        self.version = "1.0.0"
        self.available_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
        
        # Temporary data structures until teammate modules are integrated
        self.locations = {
            "Town Square": {
                "description": "The central hub of the town. People gather here to socialize and trade.",
                "connected_to": ["Marketplace", "Tavern", "Blacksmith", "Town Gate"]
            },
            "Marketplace": {
                "description": "A bustling marketplace with various vendors selling goods.",
                "connected_to": ["Town Square"]
            },
            "Tavern": {
                "description": "A cozy tavern where adventurers rest and share tales.",
                "connected_to": ["Town Square", "Tavern Cellar"]
            },
            "Blacksmith": {
                "description": "The town blacksmith's forge, where weapons and armor are crafted.",
                "connected_to": ["Town Square"]
            },
            "Town Gate": {
                "description": "The main gate leading out of town and into the wilderness.",
                "connected_to": ["Town Square", "Forest Path"]
            },
            "Forest Path": {
                "description": "A winding path through the dense forest.",
                "connected_to": ["Town Gate", "Forest Clearing"]
            },
            "Forest Clearing": {
                "description": "A clearing in the forest where sunlight breaks through.",
                "connected_to": ["Forest Path", "Deep Forest"]
            },
            "Deep Forest": {
                "description": "The deep, dark part of the forest. Beware of monsters!",
                "connected_to": ["Forest Clearing"]
            },
            "Tavern Cellar": {
                "description": "The dark cellar beneath the tavern. Rumor has it there's a secret passage.",
                "connected_to": ["Tavern"]
            }
        }
        
    def start_game(self) -> None:
        """Initialize and start the game"""
        self.clear_screen()
        self.display_welcome_message()
        self.main_menu()
    
    def clear_screen(self) -> None:
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_welcome_message(self) -> None:
        """Display the game's welcome message"""
        print("=" * 60)
        print(f"{'ADVENTURE QUEST':^60}")
        print(f"{'A Text-Based Multiplayer Adventure Game':^60}")
        print(f"{'Version ' + self.version:^60}")
        print("=" * 60)
        print(f"{'Developed by Team:':^60}")
        print(f"{'Rohit Gowda, Mohammed Irfan, Janush, Varshith, Hemanth':^60}")
        print("=" * 60)
        print("\nLoading game...\n")
        time.sleep(1)
    
    def main_menu(self) -> None:
        """Display the main menu and handle user input"""
        while self.game_running:
            self.clear_screen()
            print("\n=== MAIN MENU ===")
            print("1. New Game")
            print("2. Load Game")
            print("3. About")
            print("4. Exit")
            
  choice = input("\nEnter your choice (1-4): ")
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                self.show_about()
            elif choice == "4":
                self.exit_game()
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
    
    def new_game(self) -> None:
        """Create a new game session"""
        self.clear_screen()
        print("\n=== CHARACTER CREATION ===")
        
        player_name = input("Enter your character name: ")
        while not player_name:
            print("Name cannot be empty.")
            player_name = input("Enter your character name: ")
        
        print("\nAvailable Classes:")
        for i, class_name in enumerate(self.available_classes, 1):
            print(f"{i}. {class_name}")
        
        class_choice = 0
        while class_choice not in range(1, len(self.available_classes) + 1):
            try:
                class_choice = int(input(f"\nSelect your class (1-{len(self.available_classes)}): "))
                if class_choice not in range(1, len(self.available_classes) + 1):
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        player_class = self.available_classes[class_choice - 1]
        
        # Create a new player (will use Player class from player_module.py once integrated)
        self.active_player = TempPlayer(player_name, player_class)
        self.players[player_name] = self.active_player
        
        print(f"\nWelcome, {player_name} the {player_class}!")
        print("Your adventure begins now...")
        time.sleep(2)
        
        self.game_loop()
    
    def load_game(self) -> None:
        """Load a saved game"""
        print("\nLoading game... (Feature will be implemented in the full version)")
        print("Returning to main menu...")
        time.sleep(2)
    
    def show_about(self) -> None:
        """Display information about the game"""
        self.clear_screen()
        print("\n=== ABOUT ADVENTURE QUEST ===")
        print("Adventure Quest is a text-based multiplayer adventure game")
        print("developed as a collaborative project for a GitHub course.")
        print("\nTeam Members:")
        print("1. Rohit Gowda (Team Lead) - Main Game Controller")
        print("2. Mohammed Irfan - Player Module")
        print("3. Janush - Game World Module")
        print("4. Varshith - Items and Inventory Module")
        print("5. Hemanth - Combat System Module")
        print("\nVersion:", self.version)
        print("\nPress Enter to return to the main menu...")
        input()
    
    def exit_game(self) -> None:
        """Exit the game"""
        print("\nThank you for playing Adventure Quest!")
        print("Exiting game...")
        self.game_running = False
        time.sleep(1)
        sys.exit()
    
    def game_loop(self) -> None:
        """Main game loop"""
        in_game = True
        
        while in_game and self.game_running:
            self.clear_screen()
            player = self.active_player
            location = player.location
            location_data = self.locations[location]
            
            print(f"\n=== {location} ===")
            print(location_data["description"])
            
            print("\nWhat would you like to do?")
            print("1. View Character Stats")
            print("2. Move to a new location")
            print("3. Check Inventory")
            print("4. Save Game")
            print("5. Return to Main Menu")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice == "1":
                player.display_stats()
                input("Press Enter to continue...")
            elif choice == "2":
                self.move_player()
            elif choice == "3":
                print("\nInventory system will be integrated once teammate contributes items_inventory.py")
                input("Press Enter to continue...")
            elif choice == "4":
                print("\nSaving game... (Feature will be implemented in the full version)")
                input("Press Enter to continue...")
            elif choice == "5":
                in_game = False
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
    
    def move_player(self) -> None:
        """Handle player movement between locations"""
        player = self.active_player
        current_location = player.location
        connected_locations = self.locations[current_location]["connected_to"]
        
        print(f"\nYou are currently at: {current_location}")
        print("Connected locations:")
        
        for i, location in enumerate(connected_locations, 1):
            print(f"{i}. {location}")
        
        print(f"{len(connected_locations) + 1}. Cancel (stay here)")
        
        choice = 0
        while choice not in range(1, len(connected_locations) + 2):
            try:
                choice = int(input(f"\nWhere would you like to go? (1-{len(connected_locations) + 1}): "))
                if choice not in range(1, len(connected_locations) + 2):
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a number.")
        
        if choice == len(connected_locations) + 1:
            print("\nYou decide to stay here.")
            time.sleep(1)
            return
        
        new_location = connected_locations[choice - 1]
        player.location = new_location
        
        print(f"\nTraveling to {new_location}...")
        time.sleep(1.5)
        
        # Random encounter check (will use combat_system.py once integrated)
        if new_location not in ["Town Square", "Marketplace", "Tavern", "Blacksmith"] and random.random() < 0.3:
            print("\nA wild enemy appears! Combat system will be integrated once teammate contributes combat_system.py")
            input("Press Enter to continue...")


def main():
    """Main entry point for the game"""
    game = GameManager()
    game.start_game()


if _name_ == "_main_":
    main()