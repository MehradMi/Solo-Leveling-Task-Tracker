from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from character_class import CharacterClass

@dataclass
class Task:
    """Task model"""
    task_id: Optional[int] = None
    character_id: Optional[int] = None
    task_title: str = ""
    task_description: str = ""
    task_difficulty: str = "medium"     # easy, medium, hard, daunting (defaults to medium)
    task_category: str = "general"      # TODO: It would be nice to be able add categories at will, must implement the mechanism for it
    task_estimated_days: float = 1.0
    task_estimated_hours: float = 1.0
    task_actual_days: float = 0.0
    task_actual_hours: float = 0.0
    task_xp_reward: int = 50           # TODO: It should dynamically change with respect to the task's difficulty and the estimated time
    task_status: str = "pending"       # pending, in_progress, completed, failed
    task_priority: int = 1
    task_created_at: Optional[datetime] = None
    task_started_at: Optional[datetime] = None
    task_ended_at: Optional[datetime] = None
    task_dead_line: Optional[datetime] = None

    def calculate_xp_reward(self, character_class: str = "Technomancer") -> int:
        """Calculate XP reward based on difficulty and the actual time spent on it"""
        # TODO: Later on it would be nice to add an integrity checking system to prevent cheating in the leaderboard
        base_xp = {'easy': 25, 'medium': 50, 'hard': 100, 'daunting': 200}
        time_multiplier = max(self.task_actual_hours * 0.3, 1.0)
        class_bonus = CharacterClass.get_character_class_bonus(character_class, self.task_category)

        return int(base_xp.get(self.task_difficulty, 50) * time_multiplier * class_bonus)

    # TODO: There are some other methods left, I will implement them later

    

