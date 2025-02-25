# ui_enhancement_mod.py
from PyQt5.QtWidgets import QPushButton, QProgressBar, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

def on_game_update(game):
    # Placeholder for game update-related logic
    pass

def load_once(game):

    # Neat, organized layout with rounded corners
    game.layout.setAlignment(Qt.AlignTop)
    game.layout.setContentsMargins(25, 25, 25, 25)  # Add more space around content
    game.layout.setSpacing(20)  # Adjust space between widgets

    # Improved label for the score with a subtle shadow effect
    game.info_label.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        color: #34495e;
        background-color: #ecf0f1;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
    """)

    # Stylish buttons for all actions, using gradients and hover effects
    button_style = """
        QPushButton {
            background: linear-gradient(to right, #3498db, #2980b9);
            color: white;
            border-radius: 10px;
            font-size: 18px;
            padding: 14px;
            min-width: 160px;
        }
        QPushButton:hover {
            background: linear-gradient(to right, #2980b9, #1f6c8c);
        }
        QPushButton:pressed {
            background: linear-gradient(to right, #1f6c8c, #1a5677);
        }
    """
    
    for button in [game.click_button]:
        button.setStyleSheet(button_style)

    print("Refined UI Mod Loaded with Gradient Buttons and Polished Visuals!")

