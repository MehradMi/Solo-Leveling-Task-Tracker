from typing import Dict, List

class CharacterClass:
    """Character Class Definitions & Bonuses"""
    """Used For Showing Info To The Player, etc."""
    
    CLASSES = {
        'Technomancer': {
            'description': 'Master of code and digital realms',
            'emoji': '🧙‍♂️',
            'color': 'cyan',
            'base_stats': {
                'strength': 8,
                'intelligence': 16,
                'agility': 10,
                'focus': 14,
                'creativity': 12
            },
            'growth_stats': {
                'intelligence': 3,
                'focus': 2,
                'creativity': 1
            },
            'bonuses': {
                'Programming': 1.5,
                'Learning': 1.3,
                'Work': 1.2
            }
        },
        'Code Warrior': {
            'description': 'Battles bugs with strength and intellect',
            'emoji': '⚔️',
            'color': 'red',
            'base_stats': {
                'strength': 14,
                'intelligence': 13,
                'agility': 11,
                'focus': 12,
                'creativity': 10
            },
            'growth_stats': {
                'strength': 2,
                'intelligence': 2,
                'focus': 2
            },
            'bonuses': {
                'Programming': 1.4,
                'Work': 1.3,
                'Health': 1.2
            }
        },
        'Data Wizard': {
            'description': 'Weaves magic with data and algorithms',
            'emoji': '🧙‍♀️',
            'color': 'magenta',
            'base_stats': {
                'strength': 7,
                'intelligence': 17,
                'agility': 9,
                'focus': 13,
                'creativity': 14
            },
            'growth_stats': {
                'intelligence': 3,
                'creativity': 2,
                'focus': 1
            },
            'bonuses': {
                'Learning': 1.5,
                'Programming': 1.3,
                'Creative': 1.4
            }
        },
        'Cyber Knight': {
            'description': 'Protector of digital honor and security',
            'emoji': '🛡️',
            'color': 'blue',
            'base_stats': {
                'strength': 15,
                'intelligence': 11,
                'agility': 13,
                'focus': 13,
                'creativity': 8
            },
            'growth_stats': {
                'strength': 2,
                'agility': 2,
                'focus': 2
            },
            'bonuses': {
                'Work': 1.4,
                'Health': 1.3,
                'Social': 1.2
            }
        },
        'Digital Assassin': {
            'description': 'Swift and precise in the digital shadows',
            'emoji': '🥷',
            'color': 'yellow',
            'base_stats': {
                'strength': 10,
                'intelligence': 12,
                'agility': 16,
                'focus': 14,
                'creativity': 8
            },
            'growth_stats': {
                'agility': 3,
                'focus': 2,
                'intelligence': 1
            },
            'bonuses': {
                'Programming': 1.3,
                'Gaming': 1.5,
                'Health': 1.2
            }
        },
        'System Admin': {
            'description': 'Keeper of servers and digital infrastructure',
            'emoji': '⚙️',
            'color': 'green',
            'base_stats': {
                'strength': 11,
                'intelligence': 14,
                'agility': 9,
                'focus': 16,
                'creativity': 10
            },
            'growth_stats': {
                'focus': 3,
                'intelligence': 2,
                'strength': 1
            },
            'bonuses': {
                'Work': 1.5,
                'Programming': 1.3,
                'Learning': 1.2
            }
        }
    }

    @classmethod
    def get_character_class_info(cls, character_class_name: str) -> Dict:
        """Get certain character class information"""
        # It will return the 'Technomancer' character class info unless asked otherwise
        return cls.CLASSES.get(character_class_name, cls.CLASSES['Technomancer'])
    
    @classmethod
    def get_all_character_classes(cls) -> List[str]:
        """Get a full list of all the available character classes"""
        return list(cls.CLASSES.keys())
    
    @classmethod
    def get_character_class_bonus(cls, character_class_name: str, task_category:str) -> float:
        """Get XP bonus designated for a certain class and task category"""
        class_info = cls.get_character_class_info(character_class_name)
        return class_info['bonuses'].get(task_category)
    

