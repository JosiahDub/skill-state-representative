# built-in
import json
# 3rd party
import requests
# Mycroft stuff
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler


class StateRepresentativeSkill(MycroftSkill):
    def __init__(self):
        super(StateRepresentativeSkill, self).__init__(name="StateRepresentativeSkill")
        self.url = 'https://whoismyrepresentative.com/getall_mems.php'

    def initialize(self):
        pass

    @intent_handler(IntentBuilder("")
                    .require('StateRepresentativeKeyword')
                    .require('zip')
                    )
    def handle_state_representative(self, message):
        print("in state rep")
        zip_code = message.data.get("zip")
        result = requests.get(self.url, params={"zip": zip_code,
                                                "output": 'json'})
        if result.status_code == 200:
            content = json.loads(result.content)["results"]
        else:
            # handle it
            content = {}
        sens = []
        reps = []
        for critter in content:
            if "senate" in critter["link"]:
                sens.append(critter["name"])
            else:
                reps.append(critter["name"])
        dialog = ''
        if len(reps) == 1:
            dialog += "Your representative is " + reps[0] + "."
        elif len(reps) > 1:
            dialog += "Your representatives are " + self.oxford_comma(reps) + "."
        if len(sens) == 1:
            dialog += " Your senator is " + sens[0] + "."
        elif len(sens) == 2:
            dialog += " Your senators are " + self.oxford_comma(sens) + "."
        self.speak(dialog)

    @staticmethod
    def oxford_comma(name_list):
        if name_list == 2:
            string = name_list[0] + " and " + name_list[1]
        elif name_list > 2:
            string = ", ".join(name_list[:-1]) + ", and " + name_list[-1]
        return string

    def stop(self):
        pass


def create_skill():
    return StateRepresentativeSkill()

