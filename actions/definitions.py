"""
Store definitions used in rasa actions (e.g., related to database).
"""

DATABASE_HOST = "mysql"
DATABASE_PASSWORD = "password"
DATABASE_PORT = 3306
DATABASE_USER = "root"


# Moods, sorted by quadrant w.r.t. valence and arousal
MOODS_HA_LV = ["afraid", "alarmed", "annoyed", "distressed", "angry", 
               "frustrated"]  # high arousal, low valence
MOODS_LA_LV = ["miserable", "depressed", "gloomy", "tense", "droopy", "sad", 
               "tired", "bored", "sleepy"]  # sleepy actually in different quadrant
MOODS_LA_HV = ["content", "serene", "calm", "relaxed", "tranquil"]
MOODS_HA_HV = ["satisfied", "pleased", "delighted", "happy", "glad", 
               "astonished", "aroused", "excited"]  # high arousal, high valence