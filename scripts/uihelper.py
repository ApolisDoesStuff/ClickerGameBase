from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase

def load_once(game):
    """Applies a dark theme and loads the JetBrains font from a file to the game UI."""

    # Load the font from the assets/fonts directory
    font_path = "assets/fonts/JetBrainsMono-Regular.ttf"  # Adjust the font file name if needed

    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"Error: Could not load font from {font_path}")
    else:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        jetbrains_font = QFont(font_family, 12)  # Adjust the font size if necessary

        # Apply the font to the entire game UI
        game.setFont(jetbrains_font)

    # Dark theme stylesheet
    dark_stylesheet = """
        QWidget {
            background-color: #121212;
            color: #E0E0E0;
        }
        QPushButton {
            background-color: #333333;
            color: #FFFFFF;
            border: 2px solid #555555;
            padding: 5px;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #444444;
        }
        QPushButton:pressed {
            background-color: #222222;
        }
        QLabel {
            color: #FFFFFF;
        }
    """

    # Apply dark theme
    game.setStyleSheet(dark_stylesheet)

    print("Dark theme with custom JetBrains font applied!")
