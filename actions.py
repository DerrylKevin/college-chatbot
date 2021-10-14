# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

#rasa run -m models --enable-api --cors "*" --debug
#./ngrok http 5005
import sqlite3
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.forms import FormAction


def addComplaintToDatabase(name,number,email,comp):
    conn = sqlite3.connect('ChatBot.db')
    c = conn.cursor()
    command = "INSERT INTO Complaints VALUES(?,?,?,?)"
    pa = (name, number, email,comp)
    c.execute(command, pa)
    conn.commit()
    c.close()
    conn.close()
    return 1

class ActionBranch(Action):

    def name(self) -> Text:
        return "action_utter_branch"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        branch = ['cs', 'computer science', 'cse', 'computer science and engineering' ' civil engineering', 'civil',
                  'cv', 'mechanical engineering', 'mech',
                  'me', 'mechanical', 'is', 'is branch', 'ise', 'information science and engineering', 'eee',
                  'triple e', 'ec', 'e and c', 'e&c',
                  'ai/ml', 'ai&ml', 'artificial intelligence and machine learning',
                  'machine learning and artificial intelligence',
                  'artificial intelligence', 'machine learning', 'ai',
                  'ml', 'ai ml', 'ml/ai', 'ml ai','electronics and communications']

        b = tracker.get_slot(key="branches")
        try:
            print(b)
            if b.lower() in branch:
                s = f"Yes we offer {b} in our college"
            else:
                s = "Sorry I'm not sure!"
        except:
            s = "Sorry I'm not sure!"

        dispatcher.utter_message(text=s)

        return [AllSlotsReset()]

class ActionHostelFee(Action):

    def name(self) -> Text:
        return "action_utter_hostel_fee"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gen = tracker.get_slot(key="gender")
        try:
            print(gen)
            if gen.lower() in ['boys','boy','hudgur','hudguru','hudgur','hudugar','huduga','gand makklu','gandmakklu','hudga']:
                s = "10,000 Rupees Caution deposit + 78,000 Rupees"
            elif gen.lower() in ['girls','girl','hudgiru','hudugir','hudugiru','hudgi','hudagiru','hudagi','hudgir','henn makklu','hennmakklu']:
                s = "10,000 Rupees Caution deposit + 69,000 Rupees"
        except:
            s = "Sorry I'm not sure!"

        dispatcher.utter_message(text=s)

        return [AllSlotsReset()]

class ActionCutOff(Action):

    def name(self) -> Text:
        return "action_utter_seat_cutoffs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        b = tracker.get_slot(key="seats")
        link = 'https://vvce.ac.in/wp-content/uploads/2021/06/VVCE-Cutoff-2020.pdf'
        try:
            print(b)
            if b.lower() == 'cet':
                s = "check the cet cut off link"
            elif b.lower() in ['comedk','comed-k']:
                s = "check the comed-k cut off link"
        except:
            s = f"CET: {link}.\nCOMED-K: {link}"

        dispatcher.utter_message(text=s)

        return [AllSlotsReset()]


class ActionBranchOffered(Action):

    def name(self) -> Text:
        return "action_utter_branch_offered"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        b = tracker.get_slot(key="branch")
        try:
            print(b)
            if b.lower() in ['ug','under graduate','undergraduate']:
                s = "1.Computer Science and Engineering\n2.Computer Science and Engineering(AI & ML)\n3.Electronics and Communication Engineering\n4.Information Science and Engineering\n5.Electrical and Electronics Engineering\n6.Civil Engineering\n7.Mechanical Engineering"
            elif b.lower() in ['pg','post graduate','postgraduate']:
                s = "1. M.Tech in Computer Science\n2. M.Tech in Machine Design(Mechanical)\n3. MBA"
        except:
            s = "Sorry I'm not sure!"

        dispatcher.utter_message(text=s)

        return [AllSlotsReset()]

class ActionStudentIntake(Action):

    def name(self) -> Text:
        return "action_utter_intake_number"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        b = tracker.get_slot(key="intake")
        try:
            print(b)
            b=b.lower()
            if b in ['cs', 'computer science','cse','computer science and engineering','mechanical engineering', 'mech',
                  'me','mechanical','ec', 'e and c','e&c','electronics and communications']:
                s = f"Intake for {b} is 180."
            elif b in ['is', 'is branch','ise','information science and engineering']:
                s = f"Intake for {b} is 120."
            elif b in ['civil engineering', 'civil','cv','eee', 'triple e',
                  'ai/ml','ai&ml','artificial intelligence and machine learning','machine learning and artificial intelligence',
                  'artificial intelligence','machine learning','ai',
                  'ml','ai ml','ml/ai','ml ai']:
                s = f"Intake for {b} is 60."
        except:
            s = "Sorry I'm not sure!"

        dispatcher.utter_message(text=s)

        return [AllSlotsReset()]



class ActionTableFill(Action):

    def name(self) -> Text:
        return "action_fill_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        n=tracker.get_slot(key="name")
        nu=tracker.get_slot(key="number")
        em=tracker.get_slot(key="email")
        comp=tracker.get_slot(key="complaint")
        c=tracker.latest_message['text']
        flag=addComplaintToDatabase(n,nu,em,c)
        if flag==1:
            s=f"Name: {n}\nNumber: {nu}\nEmail: {em}\nWe have received your complaint. Our executive will contact you shortly"
        else:
            s="Sorry there was a error.Please try again after some time."
        dispatcher.utter_message(text=s)

        return [AllSlotsReset()]