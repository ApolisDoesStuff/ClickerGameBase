import sys
import os
import json
import importlib.util
try:
    from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
    from PyQt5.QtGui import QPixmap, QIcon
    from PyQt5.QtCore import Qt, QTimer
except:
    print("Error: You need to install PyQt5!")
    os.system("pause")

# Game Constants
SAVE_FILE = "savegame.json"
SCRIPTS_FOLDER = "scripts"
CLICKER_IMAGE = "assets/clicker.png"
UPGRADE_IMAGE = "assets/upgrade.png"
AUTOCLICKER_IMAGE = "assets/autoclicker.png"
PRESTIGE_IMAGE = "assets/prestige.png"

BASE_INCREMENT = 1
UPGRADE_COST = 10
UPGRADE_INCREMENT = 1
AUTOCLICKER_COST = 50
AUTOCLICKER_INCREMENT = 1
PRESTIGE_COST = 1000
PRESTIGE_MULTIPLIER_BASE = 1.5  # Base prestige multiplier

class ClickerGame(QWidget):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.increment = BASE_INCREMENT
        self.autoclickers = 0
        self.prestige_level = 0
        self.upgrade_cost = UPGRADE_COST
        self.autoclicker_cost = AUTOCLICKER_COST
        self.prestige_cost = PRESTIGE_COST
        self.prestige_multiplier = 1.0  # This will be updated based on prestige level

        self.mods = []
        self.custom_buttons = []
        self.loaded_once_mods = set()  # Track one-time mods

        self.load_game()
        self.initUI()
        self.load_mods()
        self.start_autoclicker()

        self.mod_timer = QTimer()
        self.mod_timer.timeout.connect(self.run_mods)
        self.mod_timer.start(1000)

    def initUI(self):
        self.setWindowTitle("Clicker Game with Mods")
        self.setGeometry(100, 100, 400, 500)
        
        self.layout = QVBoxLayout()
        
        self.info_label = QLabel(self.get_info_text())
        self.layout.addWidget(self.info_label)
        
        self.click_button = QPushButton()
        self.set_button_image(self.click_button, CLICKER_IMAGE)
        self.click_button.clicked.connect(self.increment_score)
        self.layout.addWidget(self.click_button, alignment=Qt.AlignCenter)

        self.save_button = QPushButton("Save Game")
        self.save_button.clicked.connect(self.save_game)
        self.layout.addWidget(self.save_button)

        self.upgrade_layout = QHBoxLayout()
        self.upgrade_button = QPushButton()
        self.set_button_image(self.upgrade_button, UPGRADE_IMAGE)
        self.upgrade_button.clicked.connect(self.upgrade)
        self.upgrade_label = QLabel(f"Cost: {self.upgrade_cost}")
        self.upgrade_layout.addWidget(self.upgrade_button)
        self.upgrade_layout.addWidget(self.upgrade_label)
        self.layout.addLayout(self.upgrade_layout)
        
        self.autoclicker_layout = QHBoxLayout()
        self.autoclicker_button = QPushButton()
        self.set_button_image(self.autoclicker_button, AUTOCLICKER_IMAGE)
        self.autoclicker_button.clicked.connect(self.buy_autoclicker)
        self.autoclicker_label = QLabel(f"Cost: {self.autoclicker_cost}")
        self.autoclicker_layout.addWidget(self.autoclicker_button)
        self.autoclicker_layout.addWidget(self.autoclicker_label)
        self.layout.addLayout(self.autoclicker_layout)
        
        self.prestige_layout = QHBoxLayout()
        self.prestige_button = QPushButton()
        self.set_button_image(self.prestige_button, PRESTIGE_IMAGE)
        self.prestige_button.clicked.connect(self.prestige)
        self.prestige_label = QLabel(f"Cost: {self.prestige_cost}")
        self.prestige_layout.addWidget(self.prestige_button)
        self.prestige_layout.addWidget(self.prestige_label)
        self.layout.addLayout(self.prestige_layout)
        
        self.setLayout(self.layout)

    def set_button_image(self, button, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Could not load image {image_path}")
        else:
            button.setIcon(QIcon(pixmap))
            button.setIconSize(pixmap.size())
            button.setStyleSheet("border: none; background: none;")

    def increment_score(self):
        self.score += self.increment * self.prestige_multiplier
        self.update_ui()

    def upgrade(self):
        if self.score >= self.upgrade_cost:
            self.score -= self.upgrade_cost
            self.increment += UPGRADE_INCREMENT
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            self.update_ui()

    def buy_autoclicker(self):
        if self.score >= self.autoclicker_cost:
            self.score -= self.autoclicker_cost
            self.autoclickers += 1
            self.autoclicker_cost = int(self.autoclicker_cost * 1.5)
            self.update_ui()

    def prestige(self):
        if self.score >= self.prestige_cost:
            self.score = 0
            self.increment = BASE_INCREMENT
            self.autoclickers = 0
            self.prestige_level += 1

            # Prestige Multiplier scales exponentially
            self.prestige_multiplier = PRESTIGE_MULTIPLIER_BASE ** self.prestige_level

            # Increase the next prestige cost
            self.prestige_cost = int(self.prestige_cost * 2.5)
            self.upgrade_cost = UPGRADE_COST
            self.autoclicker_cost = AUTOCLICKER_COST

            self.update_ui()
            print(f"Prestige! Level: {self.prestige_level}, Multiplier: {self.prestige_multiplier}, Next Prestige Cost: {self.prestige_cost}")

    def update_ui(self):
        self.info_label.setText(self.get_info_text())
        self.upgrade_label.setText(f"Cost: {self.upgrade_cost}")
        self.autoclicker_label.setText(f"Cost: {self.autoclicker_cost}")
        self.prestige_label.setText(f"Cost: {self.prestige_cost}")

    def start_autoclicker(self):
        self.autoclicker_timer = QTimer()
        self.autoclicker_timer.timeout.connect(self.run_autoclicker)
        self.autoclicker_timer.start(1000)

    def run_autoclicker(self):
        if self.autoclickers > 0:
            self.score += self.autoclickers * AUTOCLICKER_INCREMENT * self.prestige_multiplier
            self.update_ui()

    def get_info_text(self):
        return f"Score: {self.score} | Click Power: {self.increment} | AutoClickers: {self.autoclickers} | Prestige: {self.prestige_level} (x{self.prestige_multiplier:.2f})"

    def load_mods(self):
        if not os.path.exists(SCRIPTS_FOLDER):
            os.makedirs(SCRIPTS_FOLDER)
            return

        for filename in os.listdir(SCRIPTS_FOLDER):
            if filename.endswith(".py"):
                mod_path = os.path.join(SCRIPTS_FOLDER, filename)
                spec = importlib.util.spec_from_file_location(filename[:-3], mod_path)
                mod = importlib.util.module_from_spec(spec)

                try:
                    spec.loader.exec_module(mod)
                    if hasattr(mod, "on_game_update"):
                        self.mods.append(mod.on_game_update)
                    if hasattr(mod, "add_custom_button"):
                        button = mod.add_custom_button(self)
                        self.layout.addWidget(button)
                        self.custom_buttons.append(button)
                    if hasattr(mod, "load_once") and filename not in self.loaded_once_mods:
                        mod.load_once(self)
                        self.loaded_once_mods.add(filename)
                    print(f"Loaded mod: {filename}")
                except Exception as e:
                    print(f"Failed to load mod {filename}: {e}")

    def run_mods(self):
        for mod in self.mods:
            try:
                mod(self)
            except Exception as e:
                print(f"Mod error: {e}")

    def save_game(self):
        data = {
            "score": self.score,
            "increment": self.increment,
            "autoclickers": self.autoclickers,
            "prestige_level": self.prestige_level,
            "prestige_cost": self.prestige_cost,
            "upgrade_cost": self.upgrade_cost,
            "autoclicker_cost": self.autoclicker_cost
        }
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Game saved!")

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)

            self.score = data.get("score", 0)
            self.increment = data.get("increment", BASE_INCREMENT)
            self.autoclickers = data.get("autoclickers", 0)
            self.prestige_level = data.get("prestige_level", 0)
            self.prestige_cost = data.get("prestige_cost", PRESTIGE_COST)
            self.upgrade_cost = data.get("upgrade_cost", UPGRADE_COST)
            self.autoclicker_cost = data.get("autoclicker_cost", AUTOCLICKER_COST)

            # Restore prestige multiplier
            self.prestige_multiplier = PRESTIGE_MULTIPLIER_BASE ** self.prestige_level


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ClickerGame()
    game.show()
    sys.exit(app.exec_())
