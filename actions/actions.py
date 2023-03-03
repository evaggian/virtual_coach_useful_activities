# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from datetime import datetime
from definitions import (DATABASE_HOST, DATABASE_PASSWORD, 
                         DATABASE_PORT, DATABASE_USER)
from rasa_sdk import Action, FormValidationAction, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import FollowupAction, SlotSet
from typing import Any, Dict, List, Optional, Text

import mysql.connector


class ActionEndDialog(Action):
    """Action to cleanly terminate the dialog."""
    # ATM this action just call the default restart action
    # but this can be used to perform actions that might be needed
    # at the end of each dialog
    def name(self):
        return "action_end_dialog"

    async def run(self, dispatcher, tracker, domain):

        return [FollowupAction('action_restart')]


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
    
    
class ActionNameMood(Action):

    def name(self) -> Text:
        return "action_save_name_to_db"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        now = datetime.now()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

        conn = mysql.connector.connect(
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database='db'
        )
        cur = conn.cursor(prepared=True)
        query = "INSERT INTO users(prolific_id, name, time) VALUES(%s, %s, %s)"
        queryMatch = [tracker.current_state()['sender_id'], 
                      tracker.get_slot("user_name_slot"),
                      formatted_date]
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
    

class ValidateActivityExperienceForm(FormValidationAction):
    def name(self) -> Text:
        return 'validate_activity_experience_form'

    def validate_activity_experience_slot(
            self, value: Text, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # pylint: disable=unused-argument
        """Validate activity_experience_slot input."""
        last_utterance = get_latest_bot_utterance(tracker.events)

        if last_utterance != 'utter_ask_activity_experience_slot':
            return {"activity_experience_slot": None}

        # people should either type "none" or say a bit more
        if not (len(value) >= 10 or "none" in value.lower()):
            dispatcher.utter_message(response="utter_provide_more_detail")
            return {"activity_experience_slot": None}

        return {"activity_experience_slot": value}
    

class ValidateActivityExperienceModForm(FormValidationAction):
    def name(self) -> Text:
        return 'validate_activity_experience_mod_form'

    def validate_activity_experience_mod_slot(
            self, value: Text, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> Dict[Text, Any]:
        # pylint: disable=unused-argument
        """Validate activity_experience_mod_slot input."""
        last_utterance = get_latest_bot_utterance(tracker.events)

        if last_utterance != 'utter_ask_activity_experience_mod_slot':
            return {"activity_experience_slot": None}

        # people should either type "none" or say a bit more
        if not (len(value) >= 5 or "none" in value.lower()):
            dispatcher.utter_message(response="utter_provide_more_detail")
            return {"activity_experience_mod_slot": None}

        return {"activity_experience_mod_slot": value}
