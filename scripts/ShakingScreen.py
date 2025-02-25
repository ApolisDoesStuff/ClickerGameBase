from PyQt5.QtCore import QTimer, QPoint
import time
import random

SHAKE_THRESHOLD = 5
SHAKE_INTENSITY = 8
SHAKE_DURATION = 200

class ClickTracker:
    """Tracks click speed to trigger shaking."""
    def __init__(self):
        self.click_times = []

    def register_click(self):
        """Logs a click and removes old ones to keep the list fresh."""
        now = time.time()
        self.click_times.append(now)
        self.click_times = [t for t in self.click_times if now - t < 1]  # Keep only last second

    def get_clicks_per_second(self):
        """Returns number of clicks in the last second."""
        return len(self.click_times)

click_tracker = ClickTracker()

def shake_window(game):
    """Shakes the window slightly when clicking too fast."""
    original_pos = game.pos()

    def apply_shake():
        """Moves the window randomly within a small range."""
        offset_x = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        offset_y = random.randint(-SHAKE_INTENSITY, SHAKE_INTENSITY)
        game.move(original_pos + QPoint(offset_x, offset_y))

    def reset_position():
        """Resets the window back to its original position."""
        game.move(original_pos)


    if click_tracker.get_clicks_per_second() >= SHAKE_THRESHOLD:
        for i in range(5):
            QTimer.singleShot(i * (SHAKE_DURATION // 5), apply_shake)
        QTimer.singleShot(SHAKE_DURATION, reset_position)

def load_once(game):
    """Attaches the shaking effect to the click button."""
    game.click_button.clicked.connect(lambda: (click_tracker.register_click(), shake_window(game)))
    print("🔴 Shaking Screen mod loaded!")
