"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Izeal Mallory]

AI Usage: I used Google Gemini to tell me why my code wasn't running properly(why my syntax was terrible)
, to format my code in a more readable/interpretable way, and to further explain to me the
differences in the error handling exceptions. I also used it give me good and usable variable names.

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFound(f"Quest ID '{quest_id}' not found.")
    
    quest_data = quest_data_dict[quest_id]
    
    # Check not already active or completed
    if is_quest_active(character, quest_id) or is_quest_completed(character, quest_id):
        raise QuestAlreadyCompletedError(f"Quest '{quest_id}' is already active or completed.")

    # Check level requirement
    required_level = quest_data.get('REQUIRED_LEVEL', 1)
    if character.get('level', 1) < required_level:
        raise InsufficientLevelError(f"Character level is {character.get('level', 1)}, but quest requires level {required_level}.")

    # Check prerequisite (if not "NONE")
    prerequisite = quest_data.get('PREREQUISITE', 'NONE')
    if prerequisite != 'NONE':
        if not is_quest_completed(character, prerequisite):
            raise QuestRequirementsNotMetError(f"Prerequisite quest '{prerequisite}' must be completed.")

    # Add to character['active_quests']
    character['active_quests'].append(quest_id)
    return True
    pass

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    if quest_id not in quest_data_dict:
        raise QuestNotFound(f"Quest ID '{quest_id}' not found.")
        
    # Check quest is active
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active.")

    quest_data = quest_data_dict[quest_id]
    
    # Remove from active_quests
    character['active_quests'].remove(quest_id)
    
    # Add to completed_quests
    character['completed_quests'].append(quest_id)
    
    # Grant rewards (use character_manager.gain_experience and add_gold)
    reward_xp = quest_data.get('REWARD_XP', 0)
    reward_gold = quest_data.get('REWARD_GOLD', 0)
    
    character_manager.gain_experience(character, reward_xp)
    character_manager.add_gold(character, reward_gold)
    
    # Return reward summary
    return {
        'reward_xp': reward_xp,
        'reward_gold': reward_gold,
        'message': f"Quest '{quest_data['TITLE']}' completed! Gained {reward_xp} XP and {reward_gold} Gold."
    }
    pass

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    # Removes a quest from active quests without completing it
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest '{quest_id}' is not currently active and cannot be abandoned.")
        
    character['active_quests'].remove(quest_id)
    return True
    pass

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    active_quests_data = []
    
    # Look up each quest_id in character['active_quests']
    for q_id in character['active_quests']:
        if q_id in quest_data_dict:
            active_quests_data.append(quest_data_dict[q_id])
            
    # Return list of full quest data dictionaries
    return active_quests_data
    pass

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_quests_data = []
    
    for q_id in character['completed_quests']:
        if q_id in quest_data_dict:
            completed_quests_data.append(quest_data_dict[q_id])
            
    return completed_quests_data
    pass

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    available_quests = []
    
    # Filter all quests by requirements
    for quest_id, quest_data in quest_data_dict.items():
        if can_accept_quest(character, quest_id, quest_data_dict):
            # If the character meets all requirements, add the full data
            available_quests.append(quest_data)
            
    return available_quests
    pass

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    return quest_id in character['completed_quests']
    pass

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    return quest_id in character['active_quests']
    pass

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check quest exists
    if quest_id not in quest_data_dict:
        return False
        
    quest_data = quest_data_dict[quest_id]

    # Check not already active or completed
    if is_quest_active(character, quest_id) or is_quest_completed(character, quest_id):
        return False

    # Check level requirement
    required_level = quest_data.get('REQUIRED_LEVEL', 1)
    if character.get('level', 1) < required_level:
        return False

    # Check prerequisite
    prerequisite = quest_data.get('PREREQUISITE', 'NONE')
    if prerequisite != 'NONE' and not is_quest_completed(character, prerequisite):
        return False
    # Check all requirements without raising exceptions
    return True
    pass

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    if quest_id not in quest_data_dict:
        raise QuestNotFound(f"Quest ID '{quest_id}' not found.")
        
    chain = [quest_id]
    current_id = quest_id
    
    # Follow prerequisite links backwards
    while True:
        prerequisite = quest_data_dict[current_id].get('PREREQUISITE', 'NONE')
        
        if prerequisite == 'NONE':
            break
            
        if prerequisite not in quest_data_dict:
            # Handle bad data where prerequisite is not 'NONE' but doesn't exist
            # Note: This should ideally be caught by validate_quest_prerequisites
            raise QuestNotFound(f"Prerequisite '{prerequisite}' for '{current_id}' not found in data.")
            
        # Build list in reverse order
        chain.insert(0, prerequisite)
        current_id = prerequisite
        
        # Check for circular dependency (simple check: if we see the start ID again)
        if current_id == quest_id and len(chain) > 1:
            # Simple failsafe against infinite loop
            raise InvalidDataFormatError("Circular prerequisite detected in quest chain.") 
            
    return chain
    pass

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    total_quests = len(quest_data_dict)
    if total_quests == 0:
        return 0.0
        
    completed_quests = len(character['completed_quests'])
    percentage = (completed_quests / total_quests) * 100
    
    return percentage
    pass

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    total_xp = 0
    total_gold = 0
    
    completed_data = get_completed_quests(character, quest_data_dict)
    
    # Sum up reward_xp and reward_gold for all completed quests
    for quest in completed_data:
        total_xp += quest.get('REWARD_XP', 0)
        total_gold += quest.get('REWARD_GOLD', 0)
        
    return {
        'total_xp': total_xp,
        'total_gold': total_gold
    }
    pass

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    filtered_quests = []
    
    for quest_data in quest_data_dict.values():
        required_level = quest_data.get('REQUIRED_LEVEL', 1)
        
        if min_level <= required_level <= max_level:
            filtered_quests.append(quest_data)
            
    return filtered_quests
    pass

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print("--- Requirements ---")
    print(f"Level: {quest_data.get('REQUIRED_LEVEL', 1)}")
    prereq = quest_data.get('PREREQUISITE', 'NONE')
    print(f"Prerequisite: {prereq if prereq != 'NONE' else 'None'}")
    print("--- Rewards ---")
    print(f"XP: {quest_data.get('REWARD_XP', 0)}")
    print(f"Gold: {quest_data.get('REWARD_GOLD', 0)}")
    pass

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    if not quest_list:
        print("No quests to display.")
        return
        
    print("\n--- Quest List ---")
    for quest in quest_list:
        title = quest.get('TITLE', 'Unknown Quest')
        level = quest.get('REQUIRED_LEVEL', 1)
        xp = quest.get('REWARD_XP', 0)
        gold = quest.get('REWARD_GOLD', 0)
        print(f"[{level}] {title} | Rewards: {xp} XP, {gold} G")
    print("--------------------")
    pass

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    active_count = len(character['active_quests'])
    completed_count = len(character['completed_quests'])
    percentage = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    
    print(f"\n--- {character.get('name', 'Character')}'s Quest Progress ---")
    print(f"Active Quests: {active_count}")
    print(f"Completed Quests: {completed_count}")
    print(f"Total Quests Complete: {percentage:.1f}%")
    print(f"Total XP Earned: {rewards['total_xp']}")
    print(f"Total Gold Earned: {rewards['total_gold']}")
    print("---------------------------------------")
    pass

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    for quest_id, quest_data in quest_data_dict.items():
        prerequisite = quest_data.get('PREREQUISITE', 'NONE')
        
        # Ensure prerequisite exists in quest_data_dict
        if prerequisite != 'NONE' and prerequisite not in quest_data_dict:
            raise QuestNotFound(f"Invalid prerequisite: Quest '{prerequisite}' required by '{quest_id}' does not exist.")
            
    return True
    pass


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")

    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }

    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

