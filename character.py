from character_class import CharacterClass
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Character:
    """Main character class model"""
    charecter_id: Optional[int] = None
    user_id: Optional[int] = None
    name: str = ""
    character_class: str = "Technomancer"
    level: int = 1                          # When creating a character instance it will be level 1
    current_xp: int = 0
    total_xp: int = 0
    xp_to_next_level: int = 100
    stats: Dict[str, int] = None
    created_at: Optional[datetime] = None
    last_active_at: Optional[datetime] = None

    def __post_init__(self):
        if self.stats is None:
            self.stats = self.get_base_stats()

    def get_base_stats(self) -> Dict[str: int]:
        """Get base stats from the chosen character class"""
        character_class_info = CharacterClass.get_character_class_info(self.character_class)
        return character_class_info['base_stats'].copy()
    
    def calculate_leveling_xp_needed(self, level: int) -> int:
        """Calculate XP needed to reach the next level"""
        leveling_xp_factor = 1.15
        return int(100 * (leveling_xp_factor ** (level - 1)))
    
    def get_xp_progress_percentage(self) -> float:
        """Get XP progress as percentage"""
        if self.xp_to_next_level == 0:
            return 100.0
        return (self.current_xp / self.xp_to_next_level) * 100

    # TODO: There are a few methods left to add. 