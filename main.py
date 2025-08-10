#!/usr/bin/env python3
"""
Solo Leveling Task Tracker - A cyberpunk-themed personal productivity tool
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math

# Rich library for beautiful terminal output
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.table import Table
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich.layout import Layout
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Installing required dependencies...")
    os.system("pip install rich")
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, BarColumn, TextColumn
    from rich.table import Table
    from rich.prompt import Prompt, Confirm, IntPrompt
    from rich.text import Text
    from rich.layout import Layout
    from rich.align import Align

console = Console()

# Cyberpunk color scheme
CYBER_COLORS = {
    'primary': '#00ff41',      # Matrix green
    'secondary': '#ff0080',    # Cyber pink
    'accent': '#00ffff',       # Neon cyan
    'warning': '#ffff00',      # Electric yellow
    'error': '#ff0040',        # Neon red
    'dark': '#0a0a0a',         # Deep black
    'gray': '#333333'          # Dark gray
}

class Character:
    def __init__(self, name: str, character_class: str):
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        self.stats = self._init_class_stats(character_class)
        self.created_date = datetime.now().isoformat()
        
    def _init_class_stats(self, char_class: str) -> Dict[str, int]:
        """Initialize stats based on character class"""
        base_stats = {'strength': 10, 'intelligence': 10, 'agility': 10, 'focus': 10, 'creativity': 10}
        
        class_bonuses = {
            'Technomancer': {'intelligence': 5, 'focus': 3},
            'Code Warrior': {'intelligence': 4, 'strength': 3, 'focus': 2},
            'Data Wizard': {'intelligence': 6, 'creativity': 4},
            'Cyber Knight': {'strength': 4, 'agility': 3, 'focus': 3},
            'Digital Assassin': {'agility': 5, 'intelligence': 3, 'focus': 2},
            'System Admin': {'focus': 5, 'intelligence': 3, 'strength': 2}
        }
        
        if char_class in class_bonuses:
            for stat, bonus in class_bonuses[char_class].items():
                base_stats[stat] += bonus
        
        return base_stats
    
    def add_xp(self, amount: int) -> List[str]:
        """Add XP and handle level ups. Returns list of level up messages."""
        messages = []
        self.xp += amount
        
        while self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(100 * (1.2 ** (self.level - 1)))  # Exponential scaling
            messages.append(f"🚀 LEVEL UP! You are now level {self.level}!")
            
            # Stat increases on level up
            stat_increases = self._get_level_up_stats()
            for stat, increase in stat_increases.items():
                self.stats[stat] += increase
                messages.append(f"   {stat.title()} +{increase}")
        
        return messages
    
    def _get_level_up_stats(self) -> Dict[str, int]:
        """Get stat increases for level up based on class"""
        class_growth = {
            'Technomancer': {'intelligence': 2, 'focus': 1},
            'Code Warrior': {'intelligence': 1, 'strength': 1, 'focus': 1},
            'Data Wizard': {'intelligence': 2, 'creativity': 1},
            'Cyber Knight': {'strength': 1, 'agility': 1, 'focus': 1},
            'Digital Assassin': {'agility': 2, 'intelligence': 1},
            'System Admin': {'focus': 2, 'intelligence': 1}
        }
        
        return class_growth.get(self.character_class, {'focus': 1})

class Task:
    def __init__(self, title: str, description: str, difficulty: int, category: str, estimated_hours: float):
        self.id = None
        self.title = title
        self.description = description
        self.difficulty = difficulty  # 1-5 scale
        self.category = category
        self.estimated_hours = estimated_hours
        self.actual_hours = 0.0
        self.status = 'pending'  # pending, in_progress, completed, failed
        self.xp_reward = self._calculate_xp_reward()
        self.created_date = datetime.now().isoformat()
        self.completed_date = None
    
    def _calculate_xp_reward(self) -> int:
        """Calculate XP reward based on difficulty and estimated time"""
        base_xp = {1: 10, 2: 25, 3: 50, 4: 100, 5: 200}
        time_multiplier = min(self.estimated_hours * 0.5, 3.0)  # Cap at 3x multiplier
        return int(base_xp.get(self.difficulty, 50) * (1 + time_multiplier))

class Database:
    def __init__(self, db_path: str = "task_tracker.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Characters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                character_class TEXT NOT NULL,
                level INTEGER NOT NULL,
                xp INTEGER NOT NULL,
                xp_to_next INTEGER NOT NULL,
                stats TEXT NOT NULL,
                created_date TEXT NOT NULL,
                is_active BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                character_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                difficulty INTEGER NOT NULL,
                category TEXT NOT NULL,
                estimated_hours REAL NOT NULL,
                actual_hours REAL DEFAULT 0,
                status TEXT DEFAULT 'pending',
                xp_reward INTEGER NOT NULL,
                created_date TEXT NOT NULL,
                completed_date TEXT,
                FOREIGN KEY (character_id) REFERENCES characters (id)
            )
        ''')
        
        conn.commit()
        conn.close()

class TaskTracker:
    def __init__(self):
        self.db = Database()
        self.current_character = None
        self.classes = [
            'Technomancer', 'Code Warrior', 'Data Wizard', 
            'Cyber Knight', 'Digital Assassin', 'System Admin'
        ]
        self.categories = [
            'Programming', 'Learning', 'Health', 'Work', 
            'Personal', 'Creative', 'Social', 'Gaming'
        ]
    
    def display_banner(self):
        """Display the cyberpunk banner"""
        banner = Text()
        banner.append("╔═══════════════════════════════════════════════════════╗\n", style="bold cyan")
        banner.append("║  ", style="bold cyan")
        banner.append("SOLO LEVELING TASK TRACKER v1.0", style="bold magenta")
        banner.append("                 ║\n", style="bold cyan")
        banner.append("║  ", style="bold cyan")
        banner.append("「 LEVEL UP YOUR REALITY 」", style="bold green")
        banner.append("                        ║\n", style="bold cyan")
        banner.append("╚═══════════════════════════════════════════════════════╝", style="bold cyan")
        
        console.print("\n")
        console.print(Align.center(banner))
        console.print("\n")
    
    def character_creation(self) -> Character:
        """Handle character creation process"""
        console.print(Panel.fit("🎮 [bold cyan]CHARACTER CREATION PROTOCOL[/bold cyan] 🎮", 
                               border_style="cyan"))
        console.print()
        
        name = Prompt.ask("[bold yellow]Enter your character name[/bold yellow]")
        
        # Display class options
        console.print("\n[bold cyan]Available Classes:[/bold cyan]")
        for i, cls in enumerate(self.classes, 1):
            console.print(f"  {i}. [bold green]{cls}[/bold green]")
        
        console.print()
        class_choice = IntPrompt.ask(
            "[bold yellow]Select your class[/bold yellow]", 
            choices=[str(i) for i in range(1, len(self.classes) + 1)]
        )
        
        character_class = self.classes[class_choice - 1]
        character = Character(name, character_class)
        
        # Save to database
        self._save_character(character)
        
        console.print(f"\n[bold green]✓ Character '{name}' created as {character_class}![/bold green]")
        return character
    
    def _save_character(self, character: Character):
        """Save character to database"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO characters (name, character_class, level, xp, xp_to_next, stats, created_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            character.name, character.character_class, character.level, 
            character.xp, character.xp_to_next, json.dumps(character.stats),
            character.created_date, True
        ))
        
        character.id = cursor.lastrowid
        conn.commit()
        conn.close()
    
    def display_character_status(self):
        """Display current character status"""
        if not self.current_character:
            return
        
        char = self.current_character
        
        # Create progress bar for XP
        xp_progress = (char.xp / char.xp_to_next) * 100
        
        table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
        table.add_column("Character Info", style="bold yellow", width=20)
        table.add_column("Value", style="green", width=30)
        
        table.add_row("Name", char.name)
        table.add_row("Class", char.character_class)
        table.add_row("Level", str(char.level))
        table.add_row("XP", f"{char.xp}/{char.xp_to_next} ({xp_progress:.1f}%)")
        
        # Add stats
        for stat, value in char.stats.items():
            table.add_row(stat.title(), str(value))
        
        console.print(Panel(table, title="[bold cyan]Character Status[/bold cyan]", border_style="cyan"))
    
    def run(self):
        """Main application loop"""
        self.display_banner()
        
        # Check if character exists
        if not self._load_active_character():
            self.current_character = self.character_creation()
        
        while True:
            self.display_character_status()
            console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
            console.print("1. 📋 View Tasks")
            console.print("2. ➕ Add New Task")
            console.print("3. ✅ Complete Task")
            console.print("4. 👤 Character Management")
            console.print("5. 📊 View Stats")
            console.print("6. 🚪 Exit")
            
            choice = Prompt.ask("\n[bold yellow]Select option[/bold yellow]", choices=["1", "2", "3", "4", "5", "6"])
            
            if choice == "1":
                self.view_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.complete_task()
            elif choice == "4":
                self.character_management()
            elif choice == "5":
                self.view_stats()
            elif choice == "6":
                console.print("\n[bold green]Thanks for using Solo Leveling Task Tracker! Keep grinding! 🚀[/bold green]")
                break
    
    def _load_active_character(self) -> bool:
        """Load the active character from database"""
        conn = sqlite3.connect(self.db.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM characters WHERE is_active = TRUE LIMIT 1')
        row = cursor.fetchone()
        
        if row:
            char = Character(row[1], row[2])  # name, class
            char.id = row[0]
            char.level = row[3]
            char.xp = row[4]
            char.xp_to_next = row[5]
            char.stats = json.loads(row[6])
            char.created_date = row[7]
            
            self.current_character = char
            conn.close()
            return True
        
        conn.close()
        return False
    
    def view_tasks(self):
        """Display all tasks for current character"""
        # Placeholder - will implement in next iteration
        console.print(Panel.fit("[yellow]Task viewing system coming soon![/yellow]", border_style="yellow"))
    
    def add_task(self):
        """Add a new task"""
        # Placeholder - will implement in next iteration
        console.print(Panel.fit("[yellow]Task creation system coming soon![/yellow]", border_style="yellow"))
    
    def complete_task(self):
        """Mark a task as complete and award XP"""
        # Placeholder - will implement in next iteration
        console.print(Panel.fit("[yellow]Task completion system coming soon![/yellow]", border_style="yellow"))
    
    def character_management(self):
        """Manage characters"""
        # Placeholder - will implement in next iteration
        console.print(Panel.fit("[yellow]Character management coming soon![/yellow]", border_style="yellow"))
    
    def view_stats(self):
        """View character statistics and progress"""
        # Placeholder - will implement in next iteration
        console.print(Panel.fit("[yellow]Statistics viewer coming soon![/yellow]", border_style="yellow"))

if __name__ == "__main__":
    try:
        app = TaskTracker()
        app.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold red]Program terminated by user.[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]An error occurred: {e}[/bold red]")
        sys.exit(1)