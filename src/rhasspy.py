import requests
import configparser
import logging

_LOGGER = logging.getLogger(__name__)


class Rhasspy:
    def __init__(self, rhasspy_server_url, item_slot_values):
        self.rhasspy_server_url = rhasspy_server_url
        self.item_slot_values = item_slot_values

        self._syncItems()
        self._setIntents()

    def _syncItems(self):
        slot_url = "{0}/api/slots".format(self.rhasspy_server_url)

        params = dict(
            overwriteAll="true"
        )

        payload = {}

        payload['item'] = self.item_slot_values

        slot_request = requests.post(
            url=slot_url, params=params, json=payload)

        if slot_request.status_code != 200:
            _LOGGER.info("Item slot not updated: " +
                         str(slot_request.status_code))

    def _setIntents(self):
        profile_url = "{0}/api/profile?layers=all".format(
            self.rhasspy_server_url)

        params = dict(
            layers="all"
        )

        profile_request = requests.get(
            url=profile_url, params=params)

        profile = profile_request.json()

        intent_url = "{0}/api/sentences".format(self.rhasspy_server_url)

        intents = configparser.ConfigParser(allow_no_value=True)

        intents.read("/lang/{0}/sentences.ini".format(profile["language"]))

        payload = {}

        sentences = ""

        for intent in intents.sections():
            if not sentences:
                sentences = "[" + intent + "]"
            else:
                sentences = sentences + "\n\n" + "[" + intent + "]"

            for sentence in intents.options(intent):
                sentences = sentences + "\n" + sentence

        payload["intents/openHAB.ini"] = sentences

        intent_request = requests.post(
            url=intent_url, json=payload)

        if intent_request.status_code == 200:
            self._startTrain()
        else:
            _LOGGER.info("Intents not set: " + str(intent_request.status_code))

    def _startTrain(self):
        train_url = "{0}/api/train".format(self.rhasspy_server_url)
        train_request = requests.post(url=train_url)

        if train_request.status_code != 200:
            _LOGGER.info("Rhasspy not trained: " +
                         str(train_request.status_code))
