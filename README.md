# ⚔️ Gamified Productivity System 🎮

A personal productivity tracker with RPG-style gamification elements. Turn your daily tasks into an adventure and level up as you complete them!

## Features

- 📝 **Task Management**: Add, complete, and delete tasks
- 🎯 **Difficulty Levels**: Choose from easy, medium, hard, or epic tasks
- 💎 **Experience Points (XP)**: Earn XP for completing tasks
- 📈 **Leveling System**: Level up as you gain XP (100 XP per level)
- 🏆 **Achievements**: Unlock achievements as you progress
- 💾 **Data Persistence**: Your progress is saved automatically

## Installation

No installation required! Just make sure you have Python 3.6+ installed.

```bash
# Clone the repository
git clone https://github.com/helpme14/productivity_exp.git
cd productivity_exp

# Make the script executable (optional)
chmod +x productivity.py
```

## Usage

### View Dashboard

Run without arguments to see your current stats and pending tasks:

```bash
python productivity.py
```

### Add a Task

Add tasks with different difficulty levels:

```bash
# Add a medium difficulty task (default, 25 XP)
python productivity.py add "Write project documentation"

# Add an easy task (10 XP)
python productivity.py add "Reply to emails" easy

# Add a hard task (50 XP)
python productivity.py add "Refactor authentication module" hard

# Add an epic task (100 XP)
python productivity.py add "Launch new feature" epic
```

### Complete a Task

Complete tasks by their ID to earn XP:

```bash
python productivity.py complete 1
```

When you complete a task, you'll earn XP and might level up! 🎊

### List Tasks

View all your tasks:

```bash
# List pending tasks
python productivity.py list

# List all tasks (including completed)
python productivity.py list --all
```

### View Statistics

Check your progress and achievements:

```bash
python productivity.py stats
```

### Delete a Task

Remove a task you no longer need:

```bash
python productivity.py delete 1
```

## Difficulty Levels & XP

| Difficulty | XP Earned | Best For |
|------------|-----------|----------|
| Easy       | 10 XP     | Quick tasks, emails, simple updates |
| Medium     | 25 XP     | Regular tasks, moderate complexity |
| Hard       | 50 XP     | Complex tasks, significant work |
| Epic       | 100 XP    | Major milestones, big achievements |

## Achievements

Unlock achievements as you progress:

- ⭐ **First Step**: Complete your first task
- ⭐⭐ **Getting Started**: Complete 10 tasks
- ⭐⭐⭐ **Productive**: Complete 50 tasks
- 🔥 **Level 5 Achiever**: Reach level 5
- 🔥🔥 **Level 10 Master**: Reach level 10

## Data Storage

Your progress is automatically saved to `productivity_data.json` in the same directory. This file contains:
- Your current level and XP
- Total tasks completed
- All tasks (both pending and completed)

**Backup tip**: Periodically back up your `productivity_data.json` file to preserve your progress!

## Examples

```bash
# Start your productivity journey
python productivity.py add "Learn Python" medium
python productivity.py add "Exercise for 30 minutes" easy
python productivity.py add "Build a web app" epic

# Check your tasks
python productivity.py

# Complete a task
python productivity.py complete 1

# View your progress
python productivity.py stats
```

## Tips for Maximum Productivity

1. **Start Small**: Add easy tasks to build momentum
2. **Be Realistic**: Choose appropriate difficulty levels
3. **Daily Review**: Check your dashboard daily
4. **Celebrate Wins**: Enjoy those level-ups!
5. **Stay Consistent**: Regular task completion is key

## License

This is a personal project. Feel free to fork and customize it for your own use!

## Contributing

This is a personal productivity system, but suggestions are welcome! Feel free to open issues or submit pull requests.

---

**Happy Leveling! 🚀**