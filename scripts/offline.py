import time
import json
import os

SAVE_FILE = "savegame.json"

def load_once(game):
    """Handles offline earnings when the game starts."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)

            last_played = data.get("last_played", time.time())
            time_away = int(time.time() - last_played)  # Time in seconds

            if time_away > 0 and game.autoclickers > 0:
                autoclicker_increment = getattr(game, "autoclicker_increment", 1)  # Default to 1 if missing
                prestige_multiplier = getattr(game, "prestige_multiplier", 1)

                offline_earnings = game.autoclickers * autoclicker_increment * prestige_multiplier * time_away
                game.score += offline_earnings
                print(f"Welcome back! You earned {offline_earnings:.0f} points while offline for {time_away} seconds.")

        except Exception as e:
            print(f"Offline earnings mod error: {e}")

def on_game_update(game):
    """Saves last played time every update."""
    try:
        if os.path.exists(SAVE_FILE):
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {}

        data["last_played"] = time.time()

        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Failed to save last played time: {e}")
