import requests


class Item:
    def __init__(self, name, type):
        self.name = name
        self.label = None
        self.type = type
        self.synonyms = list()
        self.hasLocation = None

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class ItemNotFoundError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return str(self.__dict__)


class LocationNotFoundError(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return str(self.__dict__)


class OpenHAB:
    def __init__(self, openhab_server_url):
        self.openhab_server_url = openhab_server_url
        self.items = list()

    def switch_item(self, spoken_item, command, site_id):
        # Load all items from OpenHAB
        self._load_all_items()

        # Get the item the user requested
        item = self._get_relevant_item(spoken_item, site_id.lower())

        # Send command to item
        return self._send_command(item, command)

    def get_slot_values(self):
        # Load all items from OpenHAB
        self._load_all_items()

        # Extract slot values from items
        return self._get_slot_values()

    def _load_all_items(self):
        params = dict(
            recursive="false",
            fields="name,label,type,metadata",
            metadata="semantics,synonyms"
        )

        url = "{0}/rest/items".format(self.openhab_server_url)

        item_request = requests.get(
            url=url, params=params, verify=False)

        items = item_request.json()

        self.items.clear()

        items_with_semantics = [
            item for item in items if "metadata" in item and "semantics" in item["metadata"]]

        for item in items_with_semantics:
            current_item = Item(
                item["name"], item["type"])

            if "label" in item:
                current_item.label = item["label"].lower()

            if "synonyms" in item["metadata"]:
                current_item.synonyms = item["metadata"]["synonyms"]["value"].lower(
                ).split()

            if "config" in item["metadata"]["semantics"]:
                if "hasLocation" in item["metadata"]["semantics"]["config"]:
                    current_item.hasLocation = item["metadata"]["semantics"]["config"]["hasLocation"]

            self.items.append(current_item)

    def _get_relevant_item(self, spoken_item, site_id):
        relevant_items = list()

        location = self._get_location(site_id)

        for item in self.items:
            if item.hasLocation == location.name and (spoken_item.lower() in item.synonyms or spoken_item.lower() == item.label):
                relevant_items.append(item)

        if len(relevant_items) == 1:
            return relevant_items[0]
        else:
            raise ItemNotFoundError

    def _get_location(self, site_id):
        location = None

        for item in self.items:
            if site_id in item.synonyms or site_id == item.label:
                location = item
                return location

        if location == None:
            raise LocationNotFoundError

    def _send_command(self, item, command):
        url = "{0}/rest/items/{1}".format(self.openhab_server_url, item.name)

        request = requests.post(url=url, data=command, headers={
                                "content-type": "text/plain"}, verify=False)

        if request.status_code == 200:
            return True
        else:
            return False

    def _get_slot_values(self):
        slot_values = list()

        for item in self.items:
            slot_values.extend(item.synonyms)

            if item.label is not None:
                slot_values.append(item.label)

        slot_values = set(slot_values)

        return list(slot_values)
