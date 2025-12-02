"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Izeal Mallory]

AI Usage: I used Google Gemini to tell me why my code wasn't running properly(why my syntax was terrible),
how to reformat my 'trys' and 'excepts', help me bring my print statements together in a well
ordered manner, to format my code in a more readable/interpretable way, and to further explain to me the
differences in the error handling exceptions. I also used it give me good and usable variable names.

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    base_stats = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }
    base = base_stats[character_class]
    
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }
    
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    if character_class not in base_stats:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")
    return character
    pass

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    os.makedirs(save_directory, exist_ok=True)
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")

    try:
        data_lines = [
            f"NAME: {character['name']}",
            f"CLASS: {character['class']}",
            f"LEVEL: {character['level']}",
            f"HEALTH: {character['health']}",
            f"MAX_HEALTH: {character['max_health']}",
            f"STRENGTH: {character['strength']}",
            f"MAGIC: {character['magic']}",
            f"EXPERIENCE: {character['experience']}",
            f"GOLD: {character['gold']}",
            # Lists should be saved as comma-separated values
            f"INVENTORY: {','.join(character['inventory'])}",
            f"ACTIVE_QUESTS: {','.join(character['active_quests'])}",
            f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}",
        ]
        with open(filename, 'w') as f:
            f.write('\n'.join(data_lines))
        return True
    except (PermissionError, IOError) as e:
        raise e

#Added helper function for loading
def _parse_value(key, value):
    """Helper to convert string values back to their original type."""
    # List fields
    if key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
        return [item.strip() for item in value.split(',') if item.strip()]
    
    # Numeric fields
    if key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"]:
        try:
            return int(value)
        except ValueError:
            raise InvalidSaveDataError(f"Value for {key} is not a valid number: {value}")
    return value
    pass

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Character save file not found for: {character_name}")

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            
    except IOError as e:
        raise SaveFileCorruptedError(f"Error reading save file {filename}: {e}")

    loaded_data = {}
    required_keys_map = {
        "NAME": "name", "CLASS": "class", "LEVEL": "level", "HEALTH": "health", 
        "MAX_HEALTH": "max_health", "STRENGTH": "strength", "MAGIC": "magic", 
        "EXPERIENCE": "experience", "GOLD": "gold", "INVENTORY": "inventory", 
        "ACTIVE_QUESTS": "active_quests", "COMPLETED_QUESTS": "completed_quests"
    }
    for line in lines:
        try:
            key, value = line.strip().split(': ', 1)
            mapped_key = required_keys_map.get(key)
            if mapped_key:
                loaded_data[mapped_key] = _parse_value(key, value)
        except ValueError:
            raise InvalidSaveDataError(f"Missing required fields in save file: {line.strip()}")
    # Validate all required keys are present
    if set(required_keys_map.values()) != set(loaded_data.keys()):
        missing = set(required_keys_map.values()) - set(loaded_data.keys())
        raise InvalidSaveDataError(f"Missing required fields in save file: {', '.join(missing)}")
    
    # Final check using dedicated validation function
    validate_character_data(loaded_data)
    
    return loaded_data
    pass

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    if not os.path.isdir(save_directory):
        return []
    
    characters = []
    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            character_name = filename.rsplit('_save.txt', 1)[0]
            characters.append(character_name)
    
    return characters
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    pass

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"Cannot delete. Character file not found for: {character_name}")
    
    try:
        os.remove(filename)
        return True
    except OSError as e:
        # Catch permission issues or other OS errors
        print(f"Warning: Could not delete file {filename}: {e}")
        return False
    # Verify file exists before attempting deletion
    pass

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    if is_character_dead(character):
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain experience.")
        
    character["experience"] += xp_amount
    
    # Check for level up (can level up multiple times)
    while character["experience"] >= character["level"] * 100:
        xp_needed = character["level"] * 100
        
        # Update experience
        character["experience"] -= xp_needed
        character["level"] += 1
        
        # Update stats on level up
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        
        # Restore health to max_health
        character["health"] = character["max_health"]
        
        # print(f"*** {character['name']} leveled up to Level {character['level']}! ***") # Optional print
    pass

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError(f"Cannot spend {abs(amount)}. Resulting gold would be negative.")
        
    character["gold"] = new_gold
    return character["gold"]
    # Check that result won't be negative
    # Update character's gold
    pass

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    actual_healing = min(amount, character["max_health"] - character["health"])
    character["health"] += actual_healing
    return actual_healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    pass

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    return character.get("health", 0) <= 0
    pass

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    if not is_character_dead(character):
        return False
    revive_health = character["max_health"] // 2
    character["health"] = revive_health
    return True
    # Restore health to half of max_health
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    required_fields = {
        "name": str, "class": str, "level": int, "health": int, 
        "max_health": int, "strength": int, "magic": int, 
        "experience": int, "gold": int, "inventory": list, 
        "active_quests": list, "completed_quests": list
    }

    for field, expected_type in required_fields.items():
        # Check all required keys exist
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: {field}")
            
        # Check that values are the correct type
        value = character[field]
        if not isinstance(value, expected_type):
            raise InvalidSaveDataError(f"Field '{field}' has wrong type. Expected {expected_type.__name__}, got {type(value).__name__}")
        
        # Additional checks for numeric fields (must be non-negative, except 'health')
        if expected_type is int and field != 'health' and value < 0:
             raise InvalidSaveDataError(f"Field '{field}' cannot be negative.")

    # Check for logical inconsistencies
    if character.get('health', 0) > character.get('max_health', 1):
        raise InvalidSaveDataError(f"Health ({character['health']}) exceeds Max Health ({character['max_health']}).")
        
    if character.get('max_health', 0) <= 0:
        raise InvalidSaveDataError("Max Health must be positive.")
    return True
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
         char = create_character("TestHero", "Warrior")
         print(f"Created: {char['name']} the {char['class']}")
         print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
         print(f"Invalid class: {e}")
    
    # Test saving
    try:
         save_character(char)
         print("Character saved successfully")
    except Exception as e:
         print(f"Save error: {e}")
    
    # Test loading
    try:
         loaded = load_character("TestHero")
         print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
         print("Character not found")
    except SaveFileCorruptedError:
         print("Save file corrupted")

