# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from definitions import (DATABASE_HOST, DATABASE_PASSWORD, 
                         DATABASE_PORT, DATABASE_USER,
                         MOODS_HA_LV, MOODS_LA_LV, 
                         MOODS_LA_HV)
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Any, Dict, List, Optional, Text

import mysql.connector


def get_latest_bot_utterance(events) -> Optional[Any]:
    """
       Get the latest utterance sent by the VC.
        Args:
            events: the events list, obtained from tracker.events
        Returns:
            The name of the latest utterance
    """
    events_bot = []

    for event in events:
        if event['event'] == 'bot':
            events_bot.append(event)

    if (len(events_bot) != 0
            and 'metadata' in events_bot[-1]
            and 'utter_action' in events_bot[-1]['metadata']):
        last_utterance = events_bot[-1]['metadata']['utter_action']
    else:
        last_utterance = None

    return last_utterance


# Answer based on mood
class ActionAnswerMood(Action):
    def name(self):
        return "action_answer_mood"

    async def run(self, dispatcher, tracker, domain):

        curr_mood = tracker.get_slot('mood')

        if curr_mood == "neutral":
            dispatcher.utter_message(response="utter_mood_neutral")
        elif curr_mood in MOODS_HA_LV:
            dispatcher.utter_message(response="utter_mood_negative_valence_high_arousal_quadrant")
        elif curr_mood in MOODS_LA_LV:
            dispatcher.utter_message(response="utter_mood_negative_valence_low_arousal_quadrant")
        elif curr_mood in MOODS_LA_HV:
            dispatcher.utter_message(response="utter_mood_positive_valence_low_arousal_quadrant")
        else:
            dispatcher.utter_message(response="utter_mood_positive_valence_high_arousal_quadrant")

        return []
    
    
class ActionNameMood(Action):

    def name(self) -> Text:
        return "action_save_name_mood_to_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = mysql.connector.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database='db'
        )
        cur = conn.cursor(prepared=True)
        query = "INSERT INTO users VALUES(%s, %s, %s)"
        queryMatch = [tracker.current_state()['sender_id'], 
                      tracker.get_slot("user_name_slot"),
                      tracker.get_slot("mood")]
        cur.execute(query, queryMatch)
        conn.commit()
        conn.close()

        return []
    

class ValidateUserNameForm(FormValidationAction):
    def name(self) -> Text:
        return 'validate_user_name_form'

    def validate_user_name_slot(
            self, value: Text, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # pylint: disable=unused-argument
        """Validate user_name_slot input."""
        last_utterance = get_latest_bot_utterance(tracker.events)

        if last_utterance != 'utter_ask_user_name_slot':
            return {"user_name_slot": None}

        if not len(value) >= 2:
            return {"user_name_slot": None}

        return {"user_name_slot": value}
