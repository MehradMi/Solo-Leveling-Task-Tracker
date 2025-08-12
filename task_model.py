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
    task_difficulty: str = None     # easy, medium, hard, daunting (defaults to medium)
    task_category: str = None           # TODO: It would be nice to be able add categories at will, must implement the mechanism for it
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

    def set_task_title(self, given_task_title):
        """Users must set a title (a.k.a name) for their task, otherwise the task won't be created"""
        self.task_title = given_task_title        
        

    def set_task_description(self, given_task_description: str = ""):
        """Users can set their task description, if user input not provided, task description defaults to: 'general'"""
        self.task_description = given_task_description

        
    def set_task_category(self, given_task_category: str = "general"): 
        """Users can set their task category, if user input not provided, task category defaults to: 'general'"""
        self.task_category = given_task_category

    def set_task_difficulty(self, given_task_difficulty: str = "medium"):
        """Users can set their task diffculty, if user input not provided, task difficulty defaults to: 'medium'"""
        self.task_difficulty = given_task_difficulty

    def set_task_proiority(self, given_task_proiority: int = 1):
        """Users can set their task proiority, if user input not provided, task proiority defaults to: 1"""
        self.task_priority = given_task_proiority

    
        

    

