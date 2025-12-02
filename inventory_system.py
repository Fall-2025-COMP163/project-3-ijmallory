"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    if len(character.get('inventory', [])) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"Inventory is full. Max capacity: {MAX_INVENTORY_SIZE}")
        
    # Add item_id to character['inventory'] list
    character['inventory'].append(item_id)
    return True
    pass

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    inventory = character.get('inventory', [])
    
    # Check if item exists in inventory
    if item_id not in inventory:
        raise ItemNotFound(f"Item '{item_id}' not found in inventory.")
        
    # Remove item from list (removes the first instance)
    inventory.remove(item_id)
    return True
    pass

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    return item_id in character.get('inventory', [])
    pass

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    return character.get('inventory', []).count(item_id)
    # Use list.count() method
    pass

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    return MAX_INVENTORY_SIZE - len(character.get('inventory', []))
    pass

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    removed_items = character.get('inventory', [])[:] 
    
    # Clears character's inventory list
    character['inventory'] = []
    
    return removed_items
    # Save current inventory before clearing
    pass

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    if item_id not in character.get('inventory', []):
        raise ItemNotFound(f"Item '{item_id}' not in inventory.")
        
    item_type = item_data.get('TYPE', '').lower()
    
    # Check if item type is 'consumable'
    if item_type != 'consumable':
        raise InvalidItemTypeE(f"Item '{item_id}' is of type '{item_type}' and cannot be used. Only 'consumable' items can be used.")
        
    effect_string = item_data.get('EFFECT', '')
    
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    stat_name, value = parse_item_effect(effect_string)
    
    # Apply effect to character
    apply_stat_effect(character, stat_name, value)
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    return f"{character['name']} used {item_data['NAME']} and gained {value} {stat_name}."
    pass

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    if item_id not in character.get('inventory', []):
        raise ItemNotFound(f"Item '{item_id}' not in inventory.")
    
    if item_data.get('TYPE', '').lower() != 'weapon':
        raise InvalidItemTypeE(f"Item '{item_id}' is not a 'weapon'.")
        
    unequipped_item_id = None
    
    # Handle unequipping current weapon if exists
    if 'equipped_weapon' in character:
        unequipped_item_id = unequip_weapon(character) # This will remove bonuses and add back to inventory
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Parse effect and apply to character stats
    effect_string = item_data.get('EFFECT', '')
    stat_name, value = parse_item_effect(effect_string)
    apply_stat_effect(character, stat_name, value)
    
    # Store equipped_weapon in character dictionary
    character['equipped_weapon'] = {
        'id': item_id,
        'effect': (stat_name, value)
    }
    
    msg = f"{character['name']} equipped {item_data['NAME']}, gaining {value} {stat_name}."
    if unequipped_item_id:
        msg += f" (Unequipped {unequipped_item_id} and placed in inventory)."
        
    return msg
    pass

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    if item_id not in character.get('inventory', []):
        raise ItemNotFound(f"Item '{item_id}' not in inventory.")
    
    if item_data.get('TYPE', '').lower() != 'armor':
        raise InvalidItemTypeE(f"Item '{item_id}' is not 'armor'.")
        
    unequipped_item_id = None
    
    # Handle unequipping current armor if exists
    if 'equipped_armor' in character:
        unequipped_item_id = unequip_armor(character) # This will remove bonuses and add back to inventory
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Parse effect and apply to character stats
    effect_string = item_data.get('EFFECT', '')
    stat_name, value = parse_item_effect(effect_string)
    apply_stat_effect(character, stat_name, value)
    
    # Store equipped_armor in character dictionary
    character['equipped_armor'] = {
        'id': item_id,
        'effect': (stat_name, value)
    }
    
    msg = f"{character['name']} equipped {item_data['NAME']}, gaining {value} {stat_name}."
    if unequipped_item_id:
        msg += f" (Unequipped {unequipped_item_id} and placed in inventory)."
        
    return msg
    # Similar to equip_weapon but for armor
    pass

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    if 'equipped_weapon' not in character:
        return None # No weapon equipped
        
    weapon_data = character['equipped_weapon']
    item_id = weapon_data['id']
    stat_name, value = weapon_data['effect']
    
    # Check inventory space before removing
    if get_inventory_space_remaining(character) < 1:
        raise InventoryFullError(f"Inventory is full. Cannot unequip {item_id}.")

    # Remove stat bonuses (apply negative value)
    apply_stat_effect(character, stat_name, -value)
    
    # Add weapon back to inventory
    add_item_to_inventory(character, item_id)
    
    # Clear equipped_weapon from character
    del character['equipped_weapon']
    
    return item_id
    pass

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    if 'equipped_armor' not in character:
        return None # No armor equipped
        
    armor_data = character['equipped_armor']
    item_id = armor_data['id']
    stat_name, value = armor_data['effect']
    
    # Check inventory space before removing
    if get_inventory_space_remaining(character) < 1:
        raise InventoryFullError(f"Inventory is full. Cannot unequip {item_id}.")
        
    # Remove stat bonuses (apply negative value)
    apply_stat_effect(character, stat_name, -value)
    
    # Add armor back to inventory
    add_item_to_inventory(character, item_id)
    
    # Clear equipped_armor from character
    del character['equipped_armor']
    
    return item_id
    pass

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    cost = item_data.get('COST', 0)
    
    # Check if character has enough gold
    if character.get('gold', 0) < cost:
        raise InsufficientResourcesError(f"Cannot afford {item_data['NAME']}. Requires {cost} gold, only have {character.get('gold', 0)}.")
        
    # Check if inventory has space
    if get_inventory_space_remaining(character) < 1:
        raise InventoryFullError(f"Inventory is full. Cannot purchase {item_data['NAME']}.")
        
    # Subtract gold from character
    character['gold'] -= cost
    
    # Add item to inventory
    add_item_to_inventory(character, item_id)
    
    return True
    pass

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    if item_id not in character.get('inventory', []):
        raise ItemNotFound(f"Item '{item_id}' not found in inventory.")

    cost = item_data.get('COST', 0)
    
    # Calculate sell price (cost // 2)
    sell_price = cost // 2
    
    # Remove item from inventory
    remove_item_from_inventory(character, item_id)
    
    # Add gold to character
    character['gold'] += sell_price
    
    return sell_price
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    try:
        stat_name, value_str = effect_string.split(':', 1)
        stat_name = stat_name.strip().lower()
    except ValueError:
        raise InvalidDataFormatError(f"Invalid effect format: {effect_string}. Expected 'stat_name:value'.")
        
    # Convert value to integer
    try:
        value = int(value_str.strip())
    except ValueError:
        raise InvalidDataFormatError(f"Effect value must be an integer: {value_str}")
        
    return stat_name, value
    pass

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    valid_stats = ['health', 'max_health', 'strength', 'magic']
    
    if stat_name not in valid_stats:
        # Raise an error if stat name is invalid, though not explicitly required
        raise InvalidDataFormatError(f"Invalid stat name for effect: {stat_name}")
        
    # Add value to character[stat_name]
    character[stat_name] += value
    
    # If stat is health, ensure it doesn't exceed max_health
    if stat_name == 'health':
        character['health'] = min(character['health'], character['max_health'])
        # Also ensure health doesn't drop below 0
        character['health'] = max(character['health'], 0)
        
    # If stat is max_health, health should be checked to not exceed new max_health
    elif stat_name == 'max_health':
        character['health'] = min(character['health'], character['max_health'])
        # Also ensure max_health is not negative
        character['max_health'] = max(character['max_health'], 1)
    pass

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    inventory = character.get('inventory', [])
    item_counts = {}
    
    # Count items (some may appear multiple times)
    for item_id in inventory:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
        
    if not item_counts:
        print(f"{character['name']}'s inventory is empty.")
        return
        
    print(f"\n--- {character['name']}'s Inventory ---")
    
    # Display with item names from item_data_dict
    for item_id, count in item_counts.items():
        item_info = item_data_dict.get(item_id, {'NAME': item_id, 'TYPE': 'unknown'})
        name = item_info['NAME']
        type_ = item_info['TYPE']
        
        print(f"  {count}x {name} (Type: {type_})")
        
    print("-----------------------------------")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")

    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

