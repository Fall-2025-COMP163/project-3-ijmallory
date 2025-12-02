"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Izeal Mallory]

AI Usage: I used Google Gemini to tell me why my code wasn't running properly(why my syntax was terrible),
how to reformat my 'trys' and 'excepts', help me bring my print statements together in a well
ordered manner, to format my code in a more readable/interpretable way, and to further explain to me the
differences in the error handling exceptions.

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    print("\n--- Main Menu ---")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    
    # Get user input
    while True:
        try:
            choice = input("Enter choice (1-3): ").strip()
            # Validate input (1-3)
            choice = int(choice)
            if 1 <= choice <= 3:
                # Return choice
                return choice
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    pass

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    print("\n--- New Game Creation ---")
    
    # Get character name from user
    name = input("Enter character name: ").strip()
    if not name:
        print("Name cannot be empty. Returning to main menu.")
        return

    # Get character class from user
    while True:
        class_choice = input("Choose class (Warrior, Mage, Rogue, Cleric): ").strip().capitalize()
        try:
            # Try to create character with character_manager.create_character()
            current_character = character_manager.create_character(name, class_choice)
            break
        # Handle InvalidCharacterClassError
        except InvalidCharacterClassError as e:
            print(f"Error: {e}. Try again.")
            
    # Save character
    try:
        character_manager.save_character(current_character)
        print(f"Character '{current_character['name']}' created and saved successfully.")
        # Start game loop
        game_loop()
    except IOError as e:
        print(f"Error saving game data: {e}")
    pass

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    saved_chars = character_manager.list_saved_characters()
    
    if not saved_chars:
        print("No saved games found.")
        return

    print("\n--- Load Game ---")
    # Display them to user
    for i, name in enumerate(saved_chars, 1):
        print(f"{i}. {name}")
        
    # Get user choice
    while True:
        try:
            choice = input(f"Select character (1-{len(saved_chars)}): ").strip()
            index = int(choice) - 1
            if 0 <= index < len(saved_chars):
                char_name = saved_chars[index]
                
                # Try to load character with character_manager.load_character()
                current_character = character_manager.load_character(char_name)
                print(f"Welcome back, {current_character['name']}!")
                
                # Start game loop
                game_loop()
                return
            else:
                print("Invalid selection.")
        # Handle CharacterNotFound, SaveFileCorrupted, InvalidSaveData errors
        except (CharacterNotFound, SaveFileCorruptedError, InvalidSaveDataError) as e:
            print(f"Error loading {char_name}: {e}. Skipping this file.")
            return
        except ValueError:
            print("Invalid input. Please enter a number.")
    pass

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    while game_running:
        
        # Display game menu
        choice = game_menu()
        
        # Get player choice & Execute chosen action
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            # Save and Quit
            save_game()
            game_running = False
            print("Game saved. Thanks for playing Quest Chronicles!")
            
        # Handle death outside of battle
        if current_character and current_character.get('health', 0) <= 0:
            handle_character_death()
            
        # Save game after each action
        if game_running:
            save_game()
    pass

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    print("\n--- Game Menu ---")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    
    while True:
        try:
            choice = input("Enter choice (1-6): ").strip()
            choice = int(choice)
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    pass

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    if not current_character: return
    
    char = current_character
    print(f"\n--- {char['name']} ({char['class']}) Stats ---")
    # Show: name, class, level, health, stats, gold, etc.
    print(f"Level: {char['level']} (XP: {char['experience']})")
    print(f"Health: {char['health']}/{char['max_health']}")
    print(f"Strength: {char['strength']}, Magic: {char['magic']}")
    print(f"Gold: {char['gold']}")
    # Use character_manager functions
    # Show quest progress using quest_handler
    quest_handler.display_character_quest_progress(char, all_quests)
    pass

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    if not current_character: return
    
    while True:
        print("\n--- Inventory Menu ---")
        # Show current inventory
        inventory_system.display_inventory(current_character, all_items)
        
        print("Options: 1. Use Item, 2. Equip Weapon/Armor, 3. Drop Item, 4. Back")
        choice = input("Enter choice (1-4): ").strip()
        
        if choice == '4':
            break
            
        try:
            if choice == '1' or choice == '2':
                item_id = input("Enter item ID: ").strip()
                item_data = all_items.get(item_id)
                if not item_data:
                    print(f"Item ID '{item_id}' not recognized.")
                    continue
                    
                if choice == '1': # Use Item
                    result = inventory_system.use_item(current_character, item_id, item_data)
                    print(result)
                elif choice == '2': # Equip
                    item_type = item_data.get('TYPE', '').lower()
                    if item_type == 'weapon':
                        result = inventory_system.equip_weapon(current_character, item_id, item_data)
                        print(result)
                    elif item_type == 'armor':
                        result = inventory_system.equip_armor(current_character, item_id, item_data)
                        print(result)
                    else:
                        print(f"Item '{item_id}' cannot be equipped.")
            elif choice == '3': # Drop Item
                item_id = input("Enter item ID to drop: ").strip()
                inventory_system.remove_item_from_inventory(current_character, item_id)
                print(f"Dropped {item_id}.")
            else:
                print("Invalid option.")
        # Handle exceptions from inventory_system
        except (ItemNotFound, InvalidItemTypeE, InventoryFullError) as e:
            print(f"Inventory Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    pass

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    if not current_character: return

    while True:
        print("\n--- Quest Menu ---")
        # Show:
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back")
        
        choice = input("Enter choice (1-7): ").strip()

        if choice == '7':
            break
            
        try:
            if choice == '1':
                quest_list = quest_handler.get_active_quests(current_character, all_quests)
                quest_handler.display_quest_list(quest_list)
            elif choice == '2':
                quest_list = quest_handler.get_available_quests(current_character, all_quests)
                quest_handler.display_quest_list(quest_list)
                if quest_list:
                    q_id = input("View details (enter ID or leave blank): ").strip()
                    if q_id and q_id in all_quests:
                         quest_handler.display_quest_info(all_quests[q_id])
            elif choice == '3':
                quest_list = quest_handler.get_completed_quests(current_character, all_quests)
                quest_handler.display_quest_list(quest_list)
            elif choice == '4':
                q_id = input("Enter Quest ID to accept: ").strip()
                quest_handler.accept_quest(current_character, q_id, all_quests)
                print(f"Quest '{q_id}' accepted!")
            elif choice == '5':
                q_id = input("Enter Quest ID to abandon: ").strip()
                quest_handler.abandon_quest(current_character, q_id)
                print(f"Quest '{q_id}' abandoned.")
            elif choice == '6':
                q_id = input("Enter Active Quest ID to force complete: ").strip()
                rewards = quest_handler.complete_quest(current_character, q_id, all_quests)
                print(rewards['message'])
            else:
                print("Invalid option.")
        # Handle exceptions from quest_handler
        except (QuestNotFound, QuestRequirementsNotMetError, QuestAlreadyCompletedError, QuestNotActiveError, InsufficientLevelError) as e:
            print(f"Quest Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    pass

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    if not current_character or not combat_system.can_character_fight(current_character):
        print("You are unable to fight right now.")
        return
        
    print("\n--- Exploring... ---")
    
    # Generate random enemy based on character level
    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    print(f"A wild {enemy['name']} appears!")
    
    # Start combat with combat_system.SimpleBattle
    battle = combat_system.SimpleBattle(current_character, enemy)
    
    try:
        # Handle combat results (XP, gold, death)
        result = battle.start_battle()
        
        if result['winner'] == 'player':
            print(f"You defeated the {enemy['name']}!")
        elif result['winner'] == 'enemy':
            print("You were defeated in battle.")
            # Character death will be handled by the game_loop check
    
    # Handle exceptions
    except CharacterDeadError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected combat error occurred: {e}")
    pass

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    if not current_character: return
    
    while True:
        print("\n--- Shop ---")
        
        # Show current gold
        print(f"Current Gold: {current_character['gold']}")
        
        # Show available items for purchase (Show all available items from all_items)
        print("\nAvailable Items:")
        for item_id, data in all_items.items():
            print(f"ID: {item_id:<15} | Name: {data['NAME']:<20} | Type: {data['TYPE']:<10} | Cost: {data['COST']:<5} | Effect: {data['EFFECT']}")
            
        print("\nOptions: 1. Buy Item, 2. Sell Item, 3. Back")
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '3':
            break
            
        try:
            if choice == '1': # Buy Item
                item_id = input("Enter Item ID to buy: ").strip()
                item_data = all_items.get(item_id)
                if item_data:
                    inventory_system.purchase_item(current_character, item_id, item_data)
                    print(f"Purchased {item_data['NAME']}.")
                else:
                    print("Invalid Item ID.")
            elif choice == '2': # Sell Item
                item_id = input("Enter Item ID to sell (must be in inventory): ").strip()
                item_data = all_items.get(item_id)
                if item_data and inventory_system.has_item(current_character, item_id):
                    gold_received = inventory_system.sell_item(current_character, item_id, item_data)
                    print(f"Sold {item_data['NAME']} for {gold_received} gold.")
                else:
                    print("Item not found in inventory or Invalid Item ID.")
            else:
                print("Invalid option.")
        # Handle exceptions from inventory_system
        except (InsufficientResourcesError, InventoryFullError, ItemNotFound) as e:
            print(f"Shop Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    pass

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    if not current_character: return
    
    try:
        # Use character_manager.save_character()
        character_manager.save_character(current_character)
        # print("Game state saved.") # Print optional, saving happens after every action
    # Handle any file I/O exceptions
    except IOError as e:
        print(f"Error saving game: {e}")
    pass

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    try:
        # Try to load quests with game_data.load_quests()
        all_quests = game_data.load_quests()
        # Try to load items with game_data.load_items()
        all_items = game_data.load_items()
        
    # Handle MissingDataFileError or InvalidDataFormatError
    except MissingDataFileError:
        print("Creating default game data...")
        # If files missing, create defaults with game_data.create_default_data_files()
        game_data.create_default_data_files()
        
        # Try loading again
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
        
    except InvalidDataFormatError as e:
        # Re-raise the error to be caught by main()
        raise e
    pass

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    print("\n--------------------------------")
    print(f"!!! {current_character['name']} has fallen in battle! !!!")
    
    # Display death message
    
    # Offer: Revive (costs gold) or Quit
    revive_cost = 50 * current_character.get('level', 1)
    print(f"Options: 1. Revive (Cost: {revive_cost} Gold), 2. Quit")
    
    while True:
        choice = input("Enter choice (1 or 2): ").strip()
        
        if choice == '1':
            if current_character.get('gold', 0) >= revive_cost:
                # Use character_manager.revive_character()
                character_manager.revive_character(current_character)
                current_character['gold'] -= revive_cost
                print(f"Revived! Current HP: {current_character['health']}. Gold remaining: {current_character['gold']}")
                return # Return to game_loop
            else:
                print("Insufficient gold to revive.")
        elif choice == '2':
            # If quit: use set game_running = False
            game_running = False
            print("Game Over. Exiting Quest Chronicles.")
            return
        else:
            print("Invalid choice.")
    pass

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

