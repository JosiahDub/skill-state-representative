# built-in
import json
# 3rd party
import requests
# Mycroft stuff
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
# Our stuff
# from state_abbrev import STATE_ABBREV


class StateRepresentativeSkill(MycroftSkill):
    """
    Gives you information about your state congresspeople based on your zip code or state.

    Uses the API from whoismyrepresentative.com. ProPublica has a better and more comprehensive API,
    however it requires an API key and cannot be queried by zip code.

    Future improvements:
    * Narrowing down the representatives based on address or GPS.
    * Returning more info such as phone numbers, addresses, and party affiliations.
    * Giving local representatives such as state senators, mayors, etc.
    """
    def __init__(self):
        super(StateRepresentativeSkill, self).__init__(name="StateRepresentativeSkill")
        self.all_url = 'https://whoismyrepresentative.com/getall_mems.php'
        self.reps_url = 'https://whoismyrepresentative.com/getall_reps_bystate.php'
        self.sens_url = 'https://whoismyrepresentative.com/getall_sens_bystate.php'

    def initialize(self):
        pass

    @intent_handler(IntentBuilder("AllCongressIntent")
                    .require('congress')
                    .require('zip'))
    def handle_all_congress(self, message):
        zip_code = message.data.get("zip")
        sens = self.get_senators(zip_code=zip_code)
        reps = self.get_reps(zip_code=zip_code)
        dialog = ''
        if len(reps) == 1:
            dialog += "Your representative is " + reps[0] + "."
        elif len(reps) > 1:
            dialog += "Your representatives are " + self.oxford_comma(reps) + "."
        if len(sens) == 1:
            dialog += " Your senator is " + sens[0] + "."
        elif len(sens) == 2:
            dialog += " Your senators are " + self.oxford_comma(sens) + "."
        if not dialog:
            dialog = 'I could not find any congresspeople.'
        self.speak(dialog)

    @intent_handler(IntentBuilder("SenatorIntent")
                    .require('senator')
                    .optionally('state')
                    .optionally('zip'))
    def handle_senator(self, message):
        zip_code = message.data.get("zip", None)
        state = message.data.get("state", None)
        if zip_code is not None:
            sens = self.get_senators(zip_code=zip_code)
        elif state is not None:
            sens = self.get_senators(state=STATE_ABBREV[state])
        else:
            state = self.location['city']['state']['code']
            sens = self.get_senators(state=state)
        dialog = ''
        num_sens = len(sens)
        if num_sens == 0:
            dialog = 'I could not find any senators.'
        elif num_sens == 1:
            dialog += " Your senator is " + sens[0] + "."
        elif num_sens == 2:
            dialog += " Your senators are " + self.oxford_comma(sens) + "."
        self.speak(dialog)

    @intent_handler(IntentBuilder("RepresentativeIntent")
                    .require('representative')
                    .require('zip'))
    def handle_representatives(self, message):
        zip_code = message.data.get("zip")
        reps = self.get_reps(zip_code=zip_code)
        dialog = ''
        num_reps = len(reps)
        if num_reps == 0:
            dialog = 'I could not find any representatives.'
        elif num_reps == 1:
            dialog += "Your representative is " + reps[0] + "."
        elif num_reps > 1:
            dialog += "Your representatives are " + self.oxford_comma(reps) + "."
        self.speak(dialog)

    def get_senators(self, state=None, zip_code=None):
        if state is not None:
            result = requests.get(self.sens_url, params={"state": state,
                                                         "output": 'json'})
            if result.status_code == 200:
                try:
                    content = json.loads(result.content)["results"]
                except ValueError:
                    content = {}
            else:
                # handle it
                content = {}
            sens = [critter["name"] for critter in content]
        else:
            result = requests.get(self.all_url, params={"zip": zip_code,
                                                        "output": 'json'})
            if result.status_code == 200:
                try:
                    content = json.loads(result.content)["results"]
                except ValueError:
                    content = {}
            else:
                content = {}
            sens = []
            for critter in content:
                if "senate" in critter["link"]:
                    sens.append(critter["name"])
        return sens

    def get_reps(self, state=None, zip_code=None):
        if state is not None:
            result = requests.get(self.reps_url, params={"state": state,
                                                         "output": 'json'})
            if result.status_code == 200:
                try:
                    content = json.loads(result.content)["results"]
                except ValueError:
                    content = {}
            else:
                # handle it
                content = {}
            reps = [critter["name"] for critter in content]
        else:
            result = requests.get(self.all_url, params={"zip": zip_code,
                                                        "output": 'json'})
            if result.status_code == 200:
                try:
                    content = json.loads(result.content)["results"]
                except ValueError:
                    content = {}
            else:
                # handle it
                content = {}
            reps = []
            for critter in content:
                if "senate" not in critter["link"]:
                    reps.append(critter["name"])
        return reps

    @staticmethod
    def oxford_comma(name_list):
        num_names = len(name_list)
        if num_names == 0:
            string = ''
        elif num_names == 1:
            string = name_list[0]
        elif num_names == 2:
            string = name_list[0] + " and " + name_list[1]
        else:
            string = ", ".join(name_list[:-1]) + ", and " + name_list[-1]
        return string

    def stop(self):
        pass


STATE_ABBREV = {
    "Alabama": 	"AL",
    "Alaska": 	"AK",
    "Arizona": 	"AZ",
    "Arkansas": 	"AR",
    "California": 	"CA",
    "Colorado": 	"CO",
    "Connecticut": 	"CT",
    "Delaware": 	"DE",
    "Florida":	"FL",
    "Georgia": 	"GA",
    "Hawaii": 	"HI",
    "Idaho": 	"ID",
    "Illinois": 	"IL",
    "Indiana": 	"IN",
    "Iowa": 	"IA",
    "Kansas": 	"KS",
    "Kentucky": 	"KY",
    "Louisiana": 	"LA",
    "Maine": 	"ME",
    "Maryland": 	"MD",
    "Massachusetts": 	"MA",
    "Michigan": 	"MI",
    "Minnesota": 	"MN",
    "Mississippi": 	"MS",
    "Missouri":	"MO",
    "Montana": 	"MT",
    "Nebraska": 	"NE",
    "Nevada": 	"NV",
    "New Hampshire": 	"NH",
    "New Jersey": 	"NJ",
    "New Mexico": 	"NM",
    "New York": 	"NY",
    "North Carolina": 	"NC",
    "North Dakota": 	"ND",
    "Ohio": 	"OH",
    "Oklahoma": 	"OK",
    "Oregon": 	"OR",
    "Pennsylvania": 	"PA",
    "Rhode Island": 	"RI",
    "South Carolina": 	"SC",
    "South Dakota": 	"SD",
    "Tennessee": 	"TN",
    "Texas": 	"TX",
    "Utah": 	"UT",
    "Vermont": 	"VT",
    "Virginia": 	"VA",
    "Washington": 	"WA",
    "West Virginia": 	"WV",
    "Wisconsin": 	"WI",
    "Wyoming": "WY"
}


def create_skill():
    return StateRepresentativeSkill()
