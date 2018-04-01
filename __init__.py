from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler


class StateRepresentativeSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder().require('StateRepresentative'))
    def handle_state_representative(self, message):
        self.speak_dialog('state.representative')


def create_skill():
    return StateRepresentativeSkill()

