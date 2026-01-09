#!/usr/bin/env python3
"""
Gamified Productivity System
A personal productivity tracker with RPG-style gamification elements.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

DATA_FILE = "productivity_data.json"


class ProductivitySystem:
    """Main class for the gamified productivity system."""
    
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from JSON file or create new data structure."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load data file ({e}). Starting with fresh data.")
                return self._get_default_data()
        else:
            return self._get_default_data()
    
    def _get_default_data(self) -> Dict:
        """Return default data structure."""
        return {
            "user": {
                "level": 1,
                "xp": 0,
                "total_tasks_completed": 0
            },
            "tasks": []
        }
    
    def _save_data(self):
        """Save data to JSON file."""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except IOError as e:
            print(f"Error: Could not save data ({e}). Your changes may not be persisted.")
    
    def _calculate_level(self, xp: int) -> int:
        """Calculate level based on XP (100 XP per level)."""
        return (xp // 100) + 1
    
    def _xp_for_next_level(self, xp: int) -> int:
        """Calculate XP needed for next level."""
        current_level = self._calculate_level(xp)
        next_level_xp = current_level * 100
        return next_level_xp - xp
    
    def add_task(self, title: str, difficulty: str = "medium") -> Dict:
        """Add a new task with difficulty level."""
        xp_values = {
            "easy": 10,
            "medium": 25,
            "hard": 50,
            "epic": 100
        }
        
        # Find the next available ID
        existing_ids = [t["id"] for t in self.data["tasks"]]
        next_id = max(existing_ids) + 1 if existing_ids else 1
        
        task = {
            "id": next_id,
            "title": title,
            "difficulty": difficulty,
            "xp": xp_values.get(difficulty, 25),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        
        self.data["tasks"].append(task)
        self._save_data()
        return task
    
    def complete_task(self, task_id: int) -> Optional[Dict]:
        """Mark a task as complete and award XP."""
        for task in self.data["tasks"]:
            if task["id"] == task_id and not task["completed"]:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                
                # Award XP
                old_level = self.data["user"]["level"]
                self.data["user"]["xp"] += task["xp"]
                self.data["user"]["total_tasks_completed"] += 1
                
                # Check for level up
                new_level = self._calculate_level(self.data["user"]["xp"])
                self.data["user"]["level"] = new_level
                
                self._save_data()
                
                return {
                    "task": task,
                    "leveled_up": new_level > old_level,
                    "new_level": new_level
                }
        
        return None
    
    def list_tasks(self, show_completed: bool = False) -> List[Dict]:
        """List all tasks or only pending tasks."""
        if show_completed:
            return self.data["tasks"]
        else:
            return [t for t in self.data["tasks"] if not t["completed"]]
    
    def get_stats(self) -> Dict:
        """Get user statistics."""
        user = self.data["user"]
        pending_tasks = [t for t in self.data["tasks"] if not t["completed"]]
        completed_tasks = [t for t in self.data["tasks"] if t["completed"]]
        
        return {
            "level": user["level"],
            "xp": user["xp"],
            "xp_to_next_level": self._xp_for_next_level(user["xp"]),
            "total_tasks_completed": user["total_tasks_completed"],
            "pending_tasks": len(pending_tasks),
            "completed_tasks": len(completed_tasks)
        }
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Only pending tasks can be deleted to maintain stat integrity."""
        task_to_delete = next((t for t in self.data["tasks"] if t["id"] == task_id), None)
        
        if not task_to_delete:
            return False
        
        # Prevent deletion of completed tasks to maintain stat integrity
        if task_to_delete["completed"]:
            return False
        
        self.data["tasks"] = [t for t in self.data["tasks"] if t["id"] != task_id]
        self._save_data()
        return True


def print_banner():
    """Print the application banner."""
    print("=" * 50)
    print("    ⚔️  GAMIFIED PRODUCTIVITY SYSTEM  🎮")
    print("=" * 50)
    print()


def print_stats(system: ProductivitySystem):
    """Print user statistics in a nice format."""
    stats = system.get_stats()
    print(f"📊 Level: {stats['level']} | XP: {stats['xp']} | Next Level: {stats['xp_to_next_level']} XP")
    print(f"✅ Completed: {stats['completed_tasks']} | ⏳ Pending: {stats['pending_tasks']}")
    print()


def print_tasks(tasks: List[Dict], title: str = "Tasks"):
    """Print tasks in a formatted list."""
    if not tasks:
        print(f"No {title.lower()} found.")
        return
    
    print(f"\n{title}:")
    print("-" * 50)
    for task in tasks:
        status = "✅" if task["completed"] else "⏳"
        print(f"{status} [{task['id']}] {task['title']}")
        print(f"   Difficulty: {task['difficulty']} | XP: {task['xp']}")
    print()


def main():
    """Main CLI interface."""
    import sys
    
    system = ProductivitySystem()
    
    if len(sys.argv) < 2:
        print_banner()
        print_stats(system)
        print_tasks(system.list_tasks(), "Pending Tasks")
        print("\nUsage:")
        print("  python productivity.py add <title> [--difficulty=LEVEL]  - Add a task")
        print("  python productivity.py complete <task_id>                - Complete a task")
        print("  python productivity.py list [--all]                      - List tasks")
        print("  python productivity.py stats                             - Show statistics")
        print("  python productivity.py delete <task_id>                  - Delete a pending task")
        print("\nDifficulty levels: easy (10 XP), medium (25 XP), hard (50 XP), epic (100 XP)")
        print("Example: python productivity.py add \"Write documentation\" --difficulty=hard")
        return
    
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Task title required")
            return
        
        difficulty = "medium"
        title_parts = sys.argv[2:]
        
        # Check if --difficulty flag is used
        if any(arg.startswith("--difficulty=") for arg in sys.argv):
            for i, arg in enumerate(sys.argv):
                if arg.startswith("--difficulty="):
                    difficulty = arg.split("=", 1)[1].lower()
                    title_parts = sys.argv[2:i] + sys.argv[i+1:]
                    break
        
        # Validate difficulty
        difficulty_levels = ["easy", "medium", "hard", "epic"]
        if difficulty not in difficulty_levels:
            print(f"Error: Invalid difficulty '{difficulty}'. Use: easy, medium, hard, or epic")
            return
        
        title = " ".join(title_parts)
        if not title:
            print("Error: Task title required")
            return
        
        task = system.add_task(title, difficulty)
        print(f"✨ Task added: [{task['id']}] {task['title']} ({task['difficulty']}, {task['xp']} XP)")
    
    elif command == "complete":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            return
        
        try:
            task_id = int(sys.argv[2])
            result = system.complete_task(task_id)
            
            if result:
                print(f"🎉 Task completed: {result['task']['title']}")
                print(f"💎 Gained {result['task']['xp']} XP!")
                
                if result["leveled_up"]:
                    print(f"🎊 LEVEL UP! You are now level {result['new_level']}!")
                
                print_stats(system)
            else:
                print(f"❌ Task {task_id} not found or already completed")
        except ValueError:
            print("Error: Task ID must be a number")
    
    elif command == "list":
        show_all = "--all" in sys.argv
        tasks = system.list_tasks(show_completed=show_all)
        title = "All Tasks" if show_all else "Pending Tasks"
        print_tasks(tasks, title)
    
    elif command == "stats":
        print_banner()
        print_stats(system)
        
        stats = system.get_stats()
        print("🏆 Achievements:")
        if stats["total_tasks_completed"] >= 1:
            print("  ⭐ First Step - Complete your first task")
        if stats["total_tasks_completed"] >= 10:
            print("  ⭐⭐ Getting Started - Complete 10 tasks")
        if stats["total_tasks_completed"] >= 50:
            print("  ⭐⭐⭐ Productive - Complete 50 tasks")
        if stats["level"] >= 5:
            print("  🔥 Level 5 Achiever")
        if stats["level"] >= 10:
            print("  🔥🔥 Level 10 Master")
        print()
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Error: Task ID required")
            return
        
        try:
            task_id = int(sys.argv[2])
            if system.delete_task(task_id):
                print(f"🗑️  Task {task_id} deleted")
            else:
                # Check if task exists and is completed
                task = next((t for t in system.data["tasks"] if t["id"] == task_id), None)
                if task and task["completed"]:
                    print(f"❌ Cannot delete completed task {task_id} (stat integrity)")
                else:
                    print(f"❌ Task {task_id} not found")
        except ValueError:
            print("Error: Task ID must be a number")
    
    else:
        print(f"Unknown command: {command}")
        print("Use 'python productivity.py' to see available commands")


if __name__ == "__main__":
    main()
