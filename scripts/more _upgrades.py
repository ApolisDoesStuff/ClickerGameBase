import json
import os
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

# Define the file to store the custom upgrades data
UPGRADE_FILE = "upgrades_save.json"

# Sprite paths
SUPER_CLICK_SPRITE = "assets/super_click_sprite.png"
AUTO_BOOST_SPRITE = "assets/auto_boost_sprite.png"

def load_upgrades():
    """Load upgrades data from a separate file."""
    if os.path.exists(UPGRADE_FILE):
        with open(UPGRADE_FILE, "r") as f:
            return json.load(f)
    return {
        "super_click_cost": 30000,
        "super_click_multiplier": 2,
        "super_click_scaling": 3,
        "auto_boost_cost": 4000,
        "auto_boost_speed": 750,
        "auto_boost_scaling": 1.5
    }

def save_upgrades(upgrades):
    """Save upgrades data to the file."""
    with open(UPGRADE_FILE, "w") as f:
        json.dump(upgrades, f)

def set_button_sprite(button, image_path):
    """Set the sprite for the button."""
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        print(f"Error: Could not load image {image_path}")
    else:
        button.setIcon(QIcon(pixmap))
        button.setIconSize(pixmap.size())
        button.setStyleSheet("border: none; background: none;")

def add_custom_button(game):
    """Adds custom buttons for Super Click and Auto Boost and manages their upgrades."""

    # Load upgrade data from the separate file
    upgrades = load_upgrades()

    def buy_super_click():
        """Handle Super Click purchase logic."""
        if game.score >= upgrades["super_click_cost"]:
            game.score -= upgrades["super_click_cost"]
            game.increment *= upgrades["super_click_multiplier"]
            upgrades["super_click_cost"] = int(upgrades["super_click_cost"] * upgrades["super_click_scaling"])  # Increase cost
            super_click_label.setText(f"Cost: {upgrades['super_click_cost']}")
            game.update_ui()
            save_upgrades(upgrades)  # Save upgrades after purchase
            print(f"Super Click Purchased! New Cost: {upgrades['super_click_cost']}")

    # Super Click Button and Label
    super_click_button = QPushButton()
    set_button_sprite(super_click_button, SUPER_CLICK_SPRITE)  # Set sprite for Super Click
    super_click_button.clicked.connect(buy_super_click)
    super_click_label = QLabel(f"Cost: {upgrades['super_click_cost']}")

    super_click_layout = QHBoxLayout()
    super_click_layout.addWidget(super_click_button)
    super_click_layout.addWidget(super_click_label, alignment=Qt.AlignLeft)  # Align cost to the left
    game.layout.addLayout(super_click_layout)

    # Auto Boost purchase logic
    def buy_auto_boost():
        """Handle Auto Boost purchase logic."""
        if game.score >= upgrades["auto_boost_cost"]:
            game.score -= upgrades["auto_boost_cost"]
            new_speed = max(250, game.autoclicker_timer.interval() - upgrades["auto_boost_speed"])
            game.autoclicker_timer.setInterval(new_speed)
            upgrades["auto_boost_cost"] = int(upgrades["auto_boost_cost"] * upgrades["auto_boost_scaling"])  # Increase cost
            auto_boost_label.setText(f"Cost: {upgrades['auto_boost_cost']}")
            game.update_ui()
            save_upgrades(upgrades)  # Save upgrades after purchase
            print(f"Auto Boost Purchased! New Cost: {upgrades['auto_boost_cost']}")

    # Auto Boost Button and Label
    auto_boost_button = QPushButton()
    set_button_sprite(auto_boost_button, AUTO_BOOST_SPRITE)  # Set sprite for Auto Boost
    auto_boost_button.clicked.connect(buy_auto_boost)
    auto_boost_label = QLabel(f"Cost: {upgrades['auto_boost_cost']}")

    auto_boost_layout = QHBoxLayout()
    auto_boost_layout.addWidget(auto_boost_button)
    auto_boost_layout.addWidget(auto_boost_label, alignment=Qt.AlignLeft)  # Align cost to the left
    game.layout.addLayout(auto_boost_layout)

    return super_click_button, auto_boost_button  # Return buttons for mod compatibility
