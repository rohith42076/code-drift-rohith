#!/usr/bin/env python3
"""
Adventure Quest - Text-Based Multiplayer Adventure Game
Game World Module
Contributed by: Janush
"""

import json
import random
import time
from typing import Dict, List, Optional, Any, Union, Tuple


class Location:
    """Class representing a location in the game world"""
    def __init__(self, name: str, description: str, region: str = "Default"):
        self.name = name
        self.description = description
        self.region = region
        self.connected_locations = []
        self.npcs = []
        self.enemies = []
        self.items = []
        self.points_of_interest = {}
        self.is_safe_zone = False
        self.entry_message = ""
        self.weather = "Clear"
        self.time_of_day = "Day"
        self.discovery_text = f"You have discovered {name}!"
        self.requires_key_item = None
        self.visit_count = 0
    
    def add_connection(self, location_name: str) -> None:
        """Add a connection to another location"""
        if location_name not in self.connected_locations:
            self.connected_locations.append(location_name)
    
    def remove_connection(self, location_name: str) -> bool:
        """Remove a connection to another location"""
        if location_name in self.connected_locations:
            self.connected_locations.remove(location_name)
            return True
        return False
    
    def add_npc(self, npc: Dict[str, Any]) -> None:
        """Add an NPC to this location"""
        self.npcs.append(npc)
    
    def add_enemy(self, enemy: Dict[str, Any]) -> None:
        """Add an enemy to this location"""
        self.enemies.append(enemy)
    
    def add_item(self, item: Dict[str, Any]) -> None:
        """Add an item to this location"""
        self.items.append(item)
    
    def add_point_of_interest(self, name: str, description: str) -> None:
        """Add a point of interest to this location"""
        self.points_of_interest[name] = description
    
    def set_safe_zone(self, is_safe: bool = True) -> None:
        """Set whether this location is a safe zone (no enemies)"""
        self.is_safe_zone = is_safe
    
    def set_entry_message(self, message: str) -> None:
        """Set a custom message to display when player enters the location"""
        self.entry_message = message
    
    def set_weather(self, weather: str) -> None:
        """Set the weather at this location"""
        self.weather = weather
    
    def set_time_of_day(self, time_of_day: str) -> None:
        """Set the time of day at this location"""
        self.time_of_day = time_of_day
    
    def set_discovery_text(self, text: str) -> None:
        """Set the text displayed when a player discovers this location"""
        self.discovery_text = text
    
    def require_key_item(self, item_name: str) -> None:
        """Set an item required to access this location"""
        self.requires_key_item = item_name
    
    def visit(self) -> None:
        """Increment the visit count for this location"""
        self.visit_count += 1
    
    def get_enemies(self) -> List[Dict[str, Any]]:
        """Get list of possible enemies at this location"""
        return self.enemies
    
    def get_random_enemy(self) -> Optional[Dict[str, Any]]:
        """Get a random enemy from this location"""
        if not self.enemies or self.is_safe_zone:
            return None
        return random.choice(self.enemies)
    
    def get_description_with_details(self) -> str:
        """Get a detailed description of the location including time and weather"""
        base_desc = self.description
        
        # Add time of day and weather
        details = f"\nIt is currently {self.time_of_day.lower()}, and the weather is {self.weather.lower()}."
        
        # Add NPCs
        if self.npcs:
            npc_names = [npc["name"] for npc in self.npcs]
            if len(npc_names) == 1:
                details += f"\n{npc_names[0]} is here."
            else:
                details += f"\n{', '.join(npc_names[:-1])} and {npc_names[-1]} are here."
        
        # Add items
        if self.items:
            item_names = [item["name"] for item in self.items]
            if len(item_names) == 1:
                details += f"\nYou see a {item_names[0]} here."
            else:
                details += f"\nYou see the following items: {', '.join(item_names)}."
        
        return base_desc + details
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert location to dictionary for saving"""
        return {
            "name": self.name,
            "description": self.description,
            "region": self.region,
            "connected_locations": self.connected_locations,
            "npcs": self.npcs,
            "enemies": self.enemies,
            "items": self.items,
            "points_of_interest": self.points_of_interest,
            "is_safe_zone": self.is_safe_zone,
            "entry_message": self.entry_message,
            "weather": self.weather,
            "time_of_day": self.time_of_day,
            "discovery_text": self.discovery_text,
            "requires_key_item": self.requires_key_item,
            "visit_count": self.visit_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Location':
        """Create location from dictionary data"""
        location = cls(data["name"], data["description"], data["region"])
        location.connected_locations = data["connected_locations"]
        location.npcs = data["npcs"]
        location.enemies = data["enemies"]
        location.items = data["items"]
        location.points_of_interest = data["points_of_interest"]
        location.is_safe_zone = data["is_safe_zone"]
        location.entry_message = data["entry_message"]
        location.weather = data["weather"]
        location.time_of_day = data["time_of_day"]
        location.discovery_text = data["discovery_text"]
        location.requires_key_item = data["requires_key_item"]
        location.visit_count = data["visit_count"]
        return location


class Region:
    """Class representing a region in the game world"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.locations = []
        self.difficulty_level = 1
        self.min_player_level = 1
        self.discovery_text = f"You have discovered the {name} region!"
        self.background_music = None
        self.common_enemies = []
        self.common_items = []
    
    def add_location(self, location_name: str) -> None:
        """Add a location to this region"""
        if location_name not in self.locations:
            self.locations.append(location_name)
    
    def set_difficulty_level(self, level: int) -> None:
        """Set the difficulty level of this region"""
        self.difficulty_level = level
    
    def set_min_player_level(self, level: int) -> None:
        """Set the minimum player level recommended for this region"""
        self.min_player_level = level
    
    def set_discovery_text(self, text: str) -> None:
        """Set the text displayed when a player discovers this region"""
        self.discovery_text = text
    
    def set_background_music(self, music_file: str) -> None:
        """Set the background music for this region"""
        self.background_music = music_file
    
    def add_common_enemy(self, enemy: Dict[str, Any]) -> None:
        """Add a common enemy type for this region"""
        self.common_enemies.append(enemy)
    
    def add_common_item(self, item: Dict[str, Any]) -> None:
        """Add a common item type for this region"""
        self.common_items.append(item)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert region to dictionary for saving"""
        return {
            "name": self.name,
            "description": self.description,
            "locations": self.locations,
            "difficulty_level": self.difficulty_level,
            "min_player_level": self.min_player_level,
            "discovery_text": self.discovery_text,
            "background_music": self.background_music,
            "common_enemies": self.common_enemies,
            "common_items": self.common_items
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Region':
        """Create region from dictionary data"""
        region = cls(data["name"], data["description"])
        region.locations = data["locations"]
        region.difficulty_level = data["difficulty_level"]
        region.min_player_level = data["min_player_level"]
        region.discovery_text = data["discovery_text"]
        region.background_music = data["background_music"]
        region.common_enemies = data["common_enemies"]
        region.common_items = data["common_items"]
        return region


class World:
    """Class representing the entire game world"""
    def __init__(self):
        self.locations = {}
        self.regions = {}
        self.time_of_day = "Day"
        self.day_night_cycle_enabled = True
        self.cycle_duration = 30  # minutes in real time for a full day/night cycle
        self.current_day = 1
        self.discovered_locations = set()
        self.discovered_regions = set()
        self.save_file = "world.json"
        
    def add_location(self, location: Location) -> None:
        """Add a location to the world"""
        self.locations[location.name] = location
        
        # If the region doesn't exist, create it
        if location.region not in self.regions:
            self.regions[location.region] = Region(location.region, f"The {location.region} region")
        
        # Add location to its region
        self.regions[location.region].add_location(location.name)
    
    def add_region(self, region: Region) -> None:
        """Add a region to the world"""
        self.regions[region.name] = region
    
    def get_location(self, name: str) -> Optional[Location]:
        """Get a location by name"""
        return self.locations.get(name)
    
    def get_region(self, name: str) -> Optional[Region]:
        """Get a region by name"""
        return self.regions.get(name)
    
    def connect_locations(self, location1: str, location2: str) -> bool:
        """Create a two-way connection between locations"""
        if location1 in self.locations and location2 in self.locations:
            self.locations[location1].add_connection(location2)
            self.locations[location2].add_connection(location1)
            return True
        return False
    
    def get_connected_locations(self, location_name: str) -> List[str]:
        """Get all locations connected to a given location"""
        if location_name in self.locations:
            return self.locations[location_name].connected_locations
        return []
    
    def discover_location(self, location_name: str) -> bool:
        """Mark a location as discovered"""
        if location_name in self.locations:
            self.discovered_locations.add(location_name)
            region_name = self.locations[location_name].region
            if region_name not in self.discovered_regions:
                self.discovered_regions.add(region_name)
                return True
        return False
    
    def is_location_discovered(self, location_name: str) -> bool:
        """Check if a location has been discovered"""
        return location_name in self.discovered_locations
    
    def advance_time(self) -> None:
        """Advance the time of day"""
        if not self.day_night_cycle_enabled:
            return
            
        if self.time_of_day == "Day":
            self.time_of_day = "Dusk"
        elif self.time_of_day == "Dusk":
            self.time_of_day = "Night"
        elif self.time_of_day == "Night":
            self.time_of_day = "Dawn"
        elif self.time_of_day == "Dawn":
            self.time_of_day = "Day"
            self.current_day += 1
        
        # Update time of day for all locations
        for location in self.locations.values():
            location.set_time_of_day(self.time_of_day)
    
    def update_weather(self) -> None:
        """Update weather for all locations"""
        weather_types = ["Clear", "Cloudy", "Rainy", "Stormy", "Foggy", "Snowy", "Windy"]
        
        for location in self.locations.values():
            # 70% chance to keep current weather
            if random.random() > 0.3:
                continue
                
            # Otherwise, change weather with regional influences
            region = location.region
            if region == "Forest":
                weights = [3, 2, 3, 1, 2, 0, 1]  # More likely to be rainy or foggy
            elif region == "Mountain":
                weights = [2, 2, 1, 1, 2, 3, 3]  # More likely to be snowy or windy
            elif region == "Desert":
                weights = [5, 1, 0, 0, 0, 0, 2]  # More likely to be clear or windy
            elif region == "Swamp":
                weights = [1, 2, 3, 1, 5, 0, 0]  # More likely to be foggy or rainy
            else:
                weights = [3, 2, 2, 1, 1, 1, 2]  # Default weights
                
            weather = random.choices(weather_types, weights=weights, k=1)[0]
            location.set_weather(weather)
    
    def save_world(self) -> bool:
        """Save the world state to file"""
        try:
            # Convert locations and regions to dictionaries
            locations_dict = {name: location.to_dict() for name, location in self.locations.items()}
            regions_dict = {name: region.to_dict() for name, region in self.regions.items()}
            
            world_data = {
                "locations": locations_dict,
                "regions": regions_dict,
                "time_of_day": self.time_of_day,
                "day_night_cycle_enabled": self.day_night_cycle_enabled,
                "cycle_duration": self.cycle_duration,
                "current_day": self.current_day,
                "discovered_locations": list(self.discovered_locations),
                "discovered_regions": list(self.discovered_regions)
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(world_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving world: {str(e)}")
            return False
    
    def load_world(self) -> bool:
        """Load the world state from file"""
        try:
            with open(self.save_file, 'r') as f:
                world_data = json.load(f)
            
            # Load locations
            self.locations = {}
            for name, location_data in world_data["locations"].items():
                self.locations[name] = Location.from_dict(location_data)
            
            # Load regions
            self.regions = {}
            for name, region_data in world_data["regions"].items():
                self.regions[name] = Region.from_dict(region_data)
            
            # Load other world data
            self.time_of_day = world_data["time_of_day"]
            self.day_night_cycle_enabled = world_data["day_night_cycle_enabled"]
            self.cycle_duration = world_data["cycle_duration"]
            self.current_day = world_data["current_day"]
            self.discovered_locations = set(world_data["discovered_locations"])
            self.discovered_regions = set(world_data["discovered_regions"])
            
            return True
        except Exception as e:
            print(f"Error loading world: {str(e)}")
            return False
    
    def create_default_world(self) -> None:
        """Create a default world with predefined locations and regions"""
        # Create regions
        town_region = Region("Town", "A peaceful town surrounded by wilderness")
        forest_region = Region("Forest", "A dense forest teeming with wildlife")
        mountain_region = Region("Mountain", "Rugged mountain terrain with treacherous paths")
        
        # Set region properties
        town_region.set_difficulty_level(1)
        forest_region.set_difficulty_level(2)
        forest_region.set_min_player_level(2)
        mountain_region.set_difficulty_level(4)
        mountain_region.set_min_player_level(5)
        
        # Add regions to world
        self.add_region(town_region)
        self.add_region(forest_region)
        self.add_region(mountain_region)
        
        # Create town locations
        town_square = Location("Town Square", "The central hub of the town. People gather here to socialize and trade.", "Town")
        town_square.set_safe_zone()
        town_square.set_entry_message("You enter the bustling town square.")
        
        marketplace = Location("Marketplace", "A bustling marketplace with various vendors selling goods.", "Town")
        marketplace.set_safe_zone()
        marketplace.add_point_of_interest("General Store", "A store selling various goods.")
        marketplace.add_point_of_interest("Weapon Smith", "A blacksmith specializing in weapons.")
        marketplace.add_point_of_interest("Armor Shop", "A shop selling armor and protective gear.")
        
        tavern = Location("Tavern", "A cozy tavern where adventurers rest and share tales.", "Town")
        tavern.set_safe_zone()
        tavern.add_point_of_interest("Bar", "Where drinks are served.")
        tavern.add_point_of_interest("Fireplace", "A warm fireplace where patrons gather.")
        tavern.add_point_of_interest("Notice Board", "A board with various job postings and notices.")
        
        blacksmith = Location("Blacksmith", "The town blacksmith's forge, where weapons and armor are crafted.", "Town")
        blacksmith.set_safe_zone()
        
        town_gate = Location("Town Gate", "The main gate leading out of town and into the wilderness.", "Town")
        town_gate.set_safe_zone()
        
        # Create forest locations
        forest_path = Location("Forest Path", "A winding path through the dense forest.", "Forest")
        forest_path.set_entry_message("You enter the forest. The trees tower above you, blocking much of the sunlight.")
        
        forest_clearing = Location("Forest Clearing", "A clearing in the forest where sunlight breaks through.", "Forest")
        
        deep_forest = Location("Deep Forest", "The deep, dark part of the forest. Beware of monsters!", "Forest")
        deep_forest.set_entry_message("The forest grows darker and more threatening.")
        
        old_ruins = Location("Old Ruins", "Ancient ruins hidden deep in the forest.", "Forest")
        old_ruins.add_point_of_interest("Crumbling Tower", "A tower that looks like it might collapse.")
        old_ruins.add_point_of_interest("Stone Altar", "A strange altar with curious markings.")
        
        # Create mountain locations
        mountain_path = Location("Mountain Path", "A steep path leading up into the mountains.", "Mountain")
        mountain_path.set_entry_message("The terrain becomes rocky and steep as you begin your ascent.")
        
        mountain_cave = Location("Mountain Cave", "A dark cave in the side of the mountain.", "Mountain")
        mountain_cave.add_point_of_interest("Crystal Formation", "Beautiful crystals jut from the walls.")
        
        summit = Location("Summit", "The summit of the mountain, offering a breathtaking view.", "Mountain")
        summit.set_entry_message("After a difficult climb, you reach the summit and are rewarded with a spectacular view.")
        summit.add_point_of_interest("Viewpoint", "A perfect spot to view the lands below.")
        
        # Add enemies to appropriate locations
        forest_path.add_enemy({"name": "Wolf", "level": 2, "health": 30, "attack": 8})
        forest_clearing.add_enemy({"name": "Bear", "level": 3, "health": 50, "attack": 12})
        deep_forest.add_enemy({"name": "Forest Troll", "level": 4, "health": 70, "attack": 15})
        deep_forest.add_enemy({"name": "Dire Wolf", "level": 4, "health": 60, "attack": 18})
        old_ruins.add_enemy({"name": "Skeleton", "level": 4, "health": 45, "attack": 14})
        old_ruins.add_enemy({"name": "Ghost", "level": 5, "health": 55, "attack": 16})
        mountain_path.add_enemy({"name": "Mountain Goat", "level": 3, "health": 35, "attack": 10})
        mountain_cave.add_enemy({"name": "Cave Bat", "level": 4, "health": 30, "attack": 12})
        mountain_cave.add_enemy({"name": "Cave Troll", "level": 6, "health": 90, "attack": 20})
        
        # Add locations to world
        self.add_location(town_square)
        self.add_location(marketplace)
        self.add_location(tavern)
        self.add_location(blacksmith)
        self.add_location(town_gate)
        self.add_location(forest_path)
        self.add_location(forest_clearing)
        self.add_location(deep_forest)
        self.add_location(old_ruins)
        self.add_location(mountain_path)
        self.add_location(mountain_cave)
        self.add_location(summit)
        
        # Connect locations
        self.connect_locations("Town Square", "Marketplace")
        self.connect_locations("Town Square", "Tavern")
        self.connect_locations("Town Square", "Blacksmith")
        self.connect_locations("Town Square", "Town Gate")
        self.connect_locations("Town Gate", "Forest Path")
        self.connect_locations("Forest Path", "Forest Clearing")
        self.connect_locations("Forest Clearing", "Deep Forest")
        self.connect_locations("Deep Forest", "Old Ruins")
        self.connect_locations("Forest Clearing", "Mountain Path")
        self.connect_locations("Mountain Path", "Mountain Cave")
        self.connect_locations("Mountain Path", "Summit")
        
        # Mark Town Square as discovered
        self.discover_location("Town Square")


# Example usage of the world module (for testing)
if __name__ == "__main__":
    # Create a new world
    game_world = World()
    
    # Create a default world
    game_world.create_default_world()
    
    # Print all locations
    print("=== LOCATIONS ===")
    for name, location in game_world.locations.items():
        print(f"{name} ({location.region}): {location.description}")
        if location.connected_locations:
            print(f"  Connected to: {', '.join(location.connected_locations)}")
        if location.enemies:
            enemy_names = [enemy['name'] for enemy in location.enemies]
            print(f"  Enemies: {', '.join(enemy_names)}")
        print()
    
    # Save the world
    print("Saving world...")
    game_world.save_world()
    
    # Load the world
    print("Loading world...")
    new_world = World()
    if new_world.load_world():
        print("World loaded successfully!")
        
        # Check if Town Square exists in loaded world
        town_square = new_world.get_location("Town Square")
        if town_square:
            print(f"Town Square: {town_square.description}")
            print(f"Connected to: {', '.join(town_square.connected_locations)}")
    else:
        print("Failed to load world.")
