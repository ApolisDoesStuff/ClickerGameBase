import json
import os
from PyQt5.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QWidget, QPushButton

ACHIEVEMENTS_FILE = "achievements.json"
LEADERBOARD_FILE = "leaderboard.json"

ACHIEVEMENTS = {
    "First Click": {"condition": lambda game: game.score >= 1, "unlocked": False},
    "100 Points!": {"condition": lambda game: game.score >= 100, "unlocked": False},
    "1,000 Points!": {"condition": lambda game: game.score >= 1000, "unlocked": False},
    "First Upgrade": {"condition": lambda game: game.increment > 1, "unlocked": False},
    "First Autoclicker": {"condition": lambda game: game.autoclickers > 0, "unlocked": False},
    "First Prestige": {"condition": lambda game: game.prestige_level > 0, "unlocked": False},
}

def load_achievements():
    if os.path.exists(ACHIEVEMENTS_FILE):
        with open(ACHIEVEMENTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_achievements(achievements):
    with open(ACHIEVEMENTS_FILE, "w") as f:
        json.dump(achievements, f)

def check_achievements(game):
    unlocked = []
    saved_achievements = load_achievements()

    for name, data in ACHIEVEMENTS.items():
        if data["condition"](game) and not saved_achievements.get(name, False):
            saved_achievements[name] = True
            unlocked.append(name)

    if unlocked:
        save_achievements(saved_achievements)
        show_achievements_popup(unlocked)
        
def show_achievements_popup(achievements):
    msg = QMessageBox()
    msg.setWindowTitle("Achievements Unlocked!")
    msg.setText("\n".join(achievements))
    msg.exec_()

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(leaderboard, f)

def update_leaderboard(game):
    leaderboard = load_leaderboard()
    leaderboard.append({"score": game.score, "prestige": game.prestige_level})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # Keep top 10
    save_leaderboard(leaderboard)

def show_leaderboard(game):
    leaderboard = load_leaderboard()
    text = "\n".join([f"{i+1}. Score: {entry['score']} | Prestige: {entry['prestige']}" for i, entry in enumerate(leaderboard)])

    leaderboard_window = QWidget()
    leaderboard_window.setWindowTitle("Leaderboard")
    layout = QVBoxLayout()
    label = QLabel("Top Players:\n" + text)
    layout.addWidget(label)
    leaderboard_window.setLayout(layout)
    leaderboard_window.show()

def on_game_update(game):
    check_achievements(game)


