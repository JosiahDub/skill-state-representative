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
        for critter in content:
            print(critter["name"])
        self.speak_dialog('state.representative')

    def stop(self):
        pass


def create_skill():
    return StateRepresentativeSkill()

