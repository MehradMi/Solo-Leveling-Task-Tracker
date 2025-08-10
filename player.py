# Player Class Definition
import datetime

class Character():
    def __init__(self, name: str, character_class: str):
        self.name = name
        self.character_class = character_class
        self.level = 1 # When the character is created it's level 1
        self.xp = 0 # Players current xp amount
        self.xp_to_next = 100 # The amount of xp that player needs to level up
        self.character_creation_date = datetime.now().isoformat()

    def _init_class_stats(self, char_class: str) -> Dict[str, int]:
        """Initialize stats based on character class"""
        base_stats = {'strength': 10, 'intelligence': 10, 'agility': 10, 'focus': 10, 'creativity': 10, 'netrunning': 10}

        class_bonuses = {
            'Technomancer': {'intelligence': 5, 'netrunning': 5},
            'Code Warrior': {'intelligence': 4, }
        }

    def level_up(self):
        self.level += 1 # Level up the player character by one unit

