"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================
# Define file paths and required fields
DATA_DIR = "data"
QUESTS_FILE = os.path.join(DATA_DIR, "quests.txt")
ITEMS_FILE = os.path.join(DATA_DIR, "items.txt")

REQUIRED_QUEST_FIELDS = [
    "QUEST_ID", "TITLE", "DESCRIPTION", "REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL", "PREREQUISITE"
]
REQUIRED_ITEM_FIELDS = [
    "ITEM_ID", "NAME", "TYPE", "EFFECT", "COST", "DESCRIPTION"
]
VALID_ITEM_TYPES = ["weapon", "armor", "consumable"]
def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Data file not found: {filename}")

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except IOError as e:
        # 3. Handle Corrupted/unreadable data -> raise CorruptedDataError
        raise CorruptedDataError(f"Error reading data file {filename}: {e}")
        
    data_store = {}
    current_block = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue 

        if ':' in line:
            current_block.append(line)
        else:
            if current_block:
                try:
                    entry_dict = parse_quest_block(current_block)
                    validate_quest_data(entry_dict)
                    
                    quest_id = entry_dict["QUEST_ID"]
                    if quest_id in data_store:
                        raise InvalidDataFormatError(f"Duplicate ID found: {quest_id}")
                        
                    data_store[quest_id] = entry_dict
                except InvalidDataFormatError as e:
                    # 2. Handle Invalid format -> raise InvalidDataFormatError
                    raise InvalidDataFormatError(f"Error in {filename}: {e}")

            current_block = []

    # Process the last block
    if current_block:
        try:
            entry_dict = parse_quest_block(current_block)
            validate_quest_data(entry_dict)
            
            quest_id = entry_dict["QUEST_ID"]
            if quest_id in data_store:
                raise InvalidDataFormatError(f"Duplicate ID found: {quest_id}")
                
            data_store[quest_id] = entry_dict
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Error in {filename}: {e}")

    return data_store
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    pass

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Data file not found: {filename}")

    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except IOError as e:
        # Handles Corrupted/unreadable data -> raise CorruptedDataError
        raise CorruptedDataError(f"Error reading data file {filename}: {e}")
        
    data_store = {}
    current_block = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue 

        if ':' in line:
            current_block.append(line)
        else:
            if current_block:
                try:
                    entry_dict = parse_item_block(current_block)
                    validate_item_data(entry_dict)
                    
                    item_id = entry_dict["ITEM_ID"]
                    if item_id in data_store:
                        raise InvalidDataFormatError(f"Duplicate ID found: {item_id}")
                        
                    data_store[item_id] = entry_dict
                except InvalidDataFormatError as e:
                    # 2. Handle Invalid format -> raise InvalidDataFormatError
                    raise InvalidDataFormatError(f"Error in {filename}: {e}")

            current_block = []

    # Process the last block
    if current_block:
        try:
            entry_dict = parse_item_block(current_block)
            validate_item_data(entry_dict)
            
            item_id = entry_dict["ITEM_ID"]
            if item_id in data_store:
                raise InvalidDataFormatError(f"Duplicate ID found: {item_id}")
                
            data_store[item_id] = entry_dict
        except InvalidDataFormatError as e:
            raise InvalidDataFormatError(f"Error in {filename}: {e}")

    return data_store
    # Must handle same exceptions as load_quests
    pass

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    for field in REQUIRED_QUEST_FIELDS:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Quest missing required field: {field}")
            
    # Check that numeric values are actually numbers (and non-negative)
    numeric_fields = ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]
    for field in numeric_fields:
        value = quest_dict[field]
        if not isinstance(value, int) or value < 0:
            raise InvalidDataFormatError(f"'{field}' must be a non-negative integer.")

    return True
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    pass

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    # Checks that all required keys exist
    for field in REQUIRED_ITEM_FIELDS:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Item missing required field: {field}")

    # Checks that type is valid
    if item_dict["TYPE"].lower() not in VALID_ITEM_TYPES:
        raise InvalidDataFormatError(f"Item type '{item_dict['TYPE']}' is invalid. Must be one of: {', '.join(VALID_ITEM_TYPES)}")

    # Checks that cost is a number (and non-negative)
    cost = item_dict["COST"]
    if not isinstance(cost, int) or cost < 0:
        raise InvalidDataFormatError("COST must be a non-negative integer.")
        
    return True
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
    except OSError as e:
        # Handle any file permission errors appropriately
        print(f"Warning: Could not create directory {DATA_DIR}: {e}")
    # Create default quests.txt and items.txt files
    default_quest_data = """
# Example Quest 1
QUEST_ID: fetch_herbs
TITLE: The Missing Herbs
DESCRIPTION: Find 5 bundles of Mountain Herbs.
REWARD_XP: 50
REWARD_GOLD: 15
REQUIRED_LEVEL: 1
PREREQUISITE: NONE
"""
    default_item_data = """
# Example Item 1
ITEM_ID: iron_sword
NAME: Iron Sword
TYPE: weapon
EFFECT: damage:10
COST: 50
DESCRIPTION: A standard iron sword.
"""

    if not os.path.exists(QUESTS_FILE):
        try:
            with open(QUESTS_FILE, 'w') as f:
                f.write(default_quest_data.strip())
        except IOError as e:
            print(f"Error creating default quests file: {e}")

    if not os.path.exists(ITEMS_FILE):
        try:
            with open(ITEMS_FILE, 'w') as f:
                f.write(default_item_data.strip())
        except IOError as e:
            print(f"Error creating default items file: {e}")
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    quest = {}
    # Splits each line on ": " to get key-value pairs
    for line in lines:
        try:
            key, value = line.split(': ', 1)
            key = key.strip()
            value = value.strip()
        except ValueError:
            # Handles parsing errors gracefully
            raise InvalidDataFormatError(f"Corrupted key-value pair in quest block: {line}")

        # Converts numeric strings to integers
        if key in ["REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL"]:
            try:
                quest[key] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Value for {key} must be an integer: {value}")
        else:
            quest[key] = value
    return quest
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item = {}
    # TODO: Implement parsing logic
    for line in lines:
        try:
            key, value = line.split(': ', 1)
            key = key.strip()
            value = value.strip()
        except ValueError:
            raise InvalidDataFormatError(f"Corrupted key-value pair in item block: {line}")
        
        # Convert numeric strings to integers
        if key == "COST":
            try:
                item[key] = int(value)
            except ValueError:
                raise InvalidDataFormatError(f"Value for {key} must be an integer: {value}")
        else:
            item[key] = value
    return item
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
    #   print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
       print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

