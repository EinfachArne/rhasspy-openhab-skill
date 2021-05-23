import requests
from openhab import OpenHAB, ItemNotFoundError, LocationNotFoundError
from rhasspy import Rhasspy
from rhasspyhermes_app import EndSession, HermesApp
from rhasspyhermes.nlu import NluIntent
import argparse
import logging

logging.basicConfig(filename='/log/openHABSkill.log', level=logging.DEBUG)

_LOGGER = logging.getLogger(__name__)

parser = argparse.ArgumentParser()

# Add custom arguments
parser.add_argument("--openhabhost", default="localhost",
                    help="IP of openHAB (default: localhost)")
parser.add_argument("--openhabport", type=int,
                    default=8080, help="Port of openHAB (default: 8080)")
parser.add_argument("--rhasspyhost", default="localhost",
                    help="IP of the Rhasspy base station (default: localhost)")
parser.add_argument("--rhasspyport", type=int,
                    default=12101, help="Port of the Rhasspy base station (default: 12101)")

app = HermesApp("openHABApp", parser=parser)

args = parser.parse_args()

url_openHAB = "http://" + args.openhabhost + ":" + str(args.openhabport)

url_rhasspy = "http://" + args.rhasspyhost + ":" + str(args.rhasspyport)

openhab = OpenHAB(url_openHAB)

rhasspy = Rhasspy(url_rhasspy, openhab.get_slot_values())


@app.on_intent("OpenHABSwitchOn")
async def switchOn(intent: NluIntent):

    spoken_item = ''
    site_id = ''

    for slot in intent.slots:
        if slot.slot_name == "item":
            spoken_item = slot.value['value']

    site_id = intent.site_id

    try:
        succesful = openhab.switch_item(spoken_item, "ON", site_id)
    except ItemNotFoundError:
        return EndSession(f"{spoken_item} ist mir leider nicht bekannt")
    except LocationNotFoundError:
        return EndSession(f"{site_id} ist mir leider nicht bekannt")

    if succesful:
        return EndSession(f"{spoken_item} ist eingeschaltet")
    else:
        return EndSession(f"Ich konnte das Objekt mit dem Namen {spoken_item} leider nicht einschalten")


@app.on_intent("OpenHABSwitchOff")
async def switchOff(intent: NluIntent):

    spoken_item = ''
    site_id = ''

    for slot in intent.slots:
        if slot.slot_name == "item":
            spoken_item = slot.value['value']

    site_id = intent.site_id

    try:
        succesful = openhab.switch_item(spoken_item, "OFF", site_id)
    except ItemNotFoundError:
        return EndSession(f"{spoken_item} ist mir leider nicht bekannt")
    except LocationNotFoundError:
        return EndSession(f"{site_id} ist mir leider nicht bekannt")

    if succesful:
        return EndSession(f"{spoken_item} ist ausgeschaltet")
    else:
        return EndSession(f"Ich konnte das Objekt mit dem Namen {spoken_item} leider nicht ausschalten")

app.run()
