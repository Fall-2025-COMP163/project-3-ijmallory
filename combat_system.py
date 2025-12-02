"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Izeal Mallory]

AI Usage: I used Google Gemini to tell me why my code wasn't running properly(why my syntax was terrible),
how to reformat my 'trys' and 'excepts', help me bring my print statements together in a well
ordered manner, to format my code in a more readable/interpretable way, and to further explain to me the
differences in the error handling exceptions. I also used it give me good and usable variable names.

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================
ENEMY_BASE_STATS = {
    "goblin": {'health': 50, 'strength': 8, 'magic': 2, 'xp_reward': 25, 'gold_reward': 10},
    "orc": {'health': 80, 'strength': 12, 'magic': 5, 'xp_reward': 50, 'gold_reward': 25},
    "dragon": {'health': 200, 'strength': 25, 'magic': 15, 'xp_reward': 200, 'gold_reward': 100},
}
def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    enemy_type = enemy_type.lower()
    
    if enemy_type not in ENEMY_BASE_STATS:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' not recognized.")

    stats = ENEMY_BASE_STATS[enemy_type]
    
    # Return dictionary with name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy = {
        'name': enemy_type.capitalize(),
        'type': enemy_type,
        'health': stats['health'],
        'max_health': stats['health'],
        'strength': stats['strength'],
        'magic': stats['magic'],
        'xp_reward': stats['xp_reward'],
        'gold_reward': stats['gold_reward'],
    }
    return enemy
    pass

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else: # Level 6+
        enemy_type = "dragon"
        
    # Call create_enemy with appropriate type
    return create_enemy(enemy_type)
    pass

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        self.character = character
        self.enemy = enemy
        
        # Set combat_active flag
        self.combat_active = False
        
        # Initialize turn counter
        self.turn = 0
        pass
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        if character_manager.is_character_dead(self.character):
            raise CharacterDeadError(f"{self.character['name']} is already dead and cannot start battle.")
            
        self.combat_active = True
        display_battle_log(f"A wild {self.enemy['name']} appeared! Battle starts!")
        self.turn = 0
        
        while self.combat_active:
            self.turn += 1
            display_battle_log(f"\n--- Turn {self.turn} ---")
            
            # Player Turn
            display_combat_stats(self.character, self.enemy)
            
            # Check if enemy died before player's turn (e.g., from DOT damage if implemented)
            if self.enemy['health'] <= 0:
                self.combat_active = False
                break
                
            self.player_turn()
            
            # Check if enemy died during player's turn
            if self.enemy['health'] <= 0:
                self.combat_active = False
                break
            
            # Enemy Turn
            self.enemy_turn()
            
            # Check if character died during enemy's turn
            if character_manager.is_character_dead(self.character):
                self.combat_active = False
                break
                
        # Check battle end
        winner = self.check_battle_end()
        
        # Award XP and gold if player wins
        xp_gained = 0
        gold_gained = 0
        
        if winner == 'player':
            rewards = get_victory_rewards(self.enemy)
            xp_gained = rewards['xp']
            gold_gained = rewards['gold']
            
            character_manager.gain_experience(self.character, xp_gained)
            character_manager.add_gold(self.character, gold_gained)
            
            display_battle_log(f"VICTORY! Gained {xp_gained} XP and {gold_gained} Gold.")
        else:
            display_battle_log("DEFEAT! Better luck next time.")
        
        return {
            'winner': winner,
            'xp_gained': xp_gained,
            'gold_gained': gold_gained
        }
        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take turn outside of battle.")

        while True:
            # Display options
            print("\nPlayer Actions:")
            print("1. Basic Attack")
            # print("2. Special Ability (if available)") # Optional: Requires ability check
            print("3. Try to Run")
            
            # Get player choice
            choice = input("Choose action (1-3): ")
            
            try:
                if choice == '1':
                    damage = self.calculate_damage(self.character, self.enemy)
                    self.apply_damage(self.enemy, damage)
                    display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {damage} damage.")
                    break
                elif choice == '2':
                    try:
                        # For simplicity, I'll assume special ability is always usable here
                        log = self.use_special_ability(self.character, self.enemy)
                        display_battle_log(log)
                        break
                    except AbilityOnCooldownError as e:
                        display_battle_log(str(e))
                elif choice == '3':
                    if self.attempt_escape():
                        display_battle_log(f"{self.character['name']} successfully escaped!")
                        self.combat_active = False
                        return
                    else:
                        display_battle_log(f"{self.character['name']} failed to escape!")
                        break
                else:
                    print("Invalid choice. Try again.")
            except Exception as e:
                print(f"An error occurred during player action: {e}")
        pass
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take turn outside of battle.")
            
        display_battle_log(f"\n{self.enemy['name']}'s turn...")

        # Calculate damage
        damage = self.calculate_damage(self.enemy, self.character)
        
        # Apply to character
        self.apply_damage(self.character, damage)
        
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage.")
        pass
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        base_damage = attacker['strength']
        defense = defender['strength'] // 4
        
        damage = base_damage - defense
        
        # Minimum damage: 1
        return max(damage, 1)
        pass
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        # Reduct health
        target['health'] -= damage
        
        # Prevents negative health
        target['health'] = max(target['health'], 0)
        pass
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        
        if character_manager.is_character_dead(self.character):
            self.combat_active = False
            return 'enemy'
            
        return None
        pass
    
    import random
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        if random.random() < 0.5:
            # If successful, set combat_active to False (done in player_turn)
            return True
        else:
            return False
        pass

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    char_class = character['class'].lower()
    current_turn = character.get('current_battle_turn', 0)
    last_use_turn = character.get('last_ability_turn', -ABILITY_COOLDOWN_TURNS)
    
    if current_turn - last_use_turn < ABILITY_COOLDOWN_TURNS:
        
        # Raise AbilityOnCooldownError if ability was used recently
        turns_left = ABILITY_COOLDOWN_TURNS - (current_turn - last_use_turn)
        raise AbilityOnCooldownError(f"Special ability is on cooldown. Wait {turns_left} more turn(s).")
        
        # Check character class and execute appropriate ability
        if char_class == 'warrior':
            return warrior_power_strike(character, enemy)
        elif char_class == 'mage':
            return mage_fireball(character, enemy)
        elif char_class == 'rogue':
            return rogue_critical_strike(character, enemy)
        elif char_class == 'cleric':
            return cleric_heal(character)
        else:
            return "No special ability available for this class."
    pass

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    base_damage = character['strength'] * 2
    defense = enemy['strength'] // 4
    damage = max(base_damage - defense, 1)
    
    # Apply damage
    SimpleBattle.apply_damage(None, enemy, damage)
    return f"WARRIOR uses Power Strike! Hits {enemy['name']} for {damage} damage."
    pass

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    base_damage = character['magic'] * 2
    # Mage attacks often ignore physical defense, using 0 defense for simplicity
    damage = max(base_damage, 1) 
    
    # Apply damage
    SimpleBattle.apply_damage(None, enemy, damage)
    
    return f"MAGE casts Fireball! Blasts {enemy['name']} for {damage} magic damage."
    pass

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    if random.random() < 0.5:
        # Critical Hit (3x strength damage)
        base_damage = character['strength'] * 3
        crit_text = "CRITICAL HIT"
    else:
        # Normal Hit (1x strength damage)
        base_damage = character['strength']
        crit_text = "normal strike"

    defense = enemy['strength'] // 4
    damage = max(base_damage - defense, 1)
    
    # Apply damage
    SimpleBattle.apply_damage(None, enemy, damage)
    
    return f"ROGUE performs a {crit_text}! Hits {enemy['name']} for {damage} damage."
    pass

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    heal_amount = 30
    # A function that correctly caps healing at max_health
    actual_healing = min(heal_amount, character['max_health'] - character['health'])
    character['health'] += actual_healing
    return f"CLERIC restores {actual_healing} health. Current HP: {character['health']}/{character['max_health']}."
    pass

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character['health'] > 0
    pass

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    return {
        'xp': enemy.get('xp_reward', 0),
        'gold': enemy.get('gold_reward', 0)
    }
    pass

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    pass

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

