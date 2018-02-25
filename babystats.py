import json
import urllib.request

myID = "1038505942"
myaccessToken = "2018-02-25:a02cf622-9ded-4bc6-ae30-846fcca363db"

conditionsSetURL = 'https://www.babystats.org/api/public'

babystat_commands = [
    "add wet",
    "add feeding",
    "start feeding",
    "end feeding",
    "stop feeding",
    "add stool",
    "add weight",
    "add note",
    "add sleep",
    "add pumping",
    "add kick",
    "start sleep",
    "end sleep",
    "stop sleep",
    "remove wet",
    "remove feeding",
    "remove stool",
    "remove weight",
    "remove note",
    "remove sleep",
    "remove kick",
    "remove pumping",
    "last feeding",
    "last wet",
    "last stool",
    "last sleep",
    "last weight",
    "last pumping",
    "last kick",
    "get stat",
    "get data",
    "get transactiondata",
    "get countdata",
]

single_event_text = [
    "add wet",
    "stop feeding",
    "add stool",
    "add kick",
    "start sleep",
    "end sleep",
    "stop sleep",
    "remove wet",
    "remove feeding",
    "remove stool",
    "remove weight",
    "remove note",
    "remove sleep",
    "remove kick",
    "remove pumping",
    "last feeding",
    "last wet",
    "last stool",
    "last sleep",
    "last weight",
    "last pumping",
    "last kick",
]


def single_event(spoken_text):
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": spoken_text.title().replace(' ',''),
        "babyName" : "",
        "eventTime" : ""
    }


def add_pumping(spoken_text):
    volume = spoken_text.replace("add pumping", "").strip()
    #!!!!! NEED TO CONVERT VOLUME TO FLOAT
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": "AddPumping",
        "bottleOunces": volume,
        "babyName" : "",
        "eventTime" : ""
    }


def feeding(spoken_text):
    breast_or_volume = spoken_text.replace("add feeding", "").replace("start feeding", "").replace("end feeding", "").strip()
    breastSide = ""
    for b in ['left', 'right', 'both']:
        if b in breast_or_volume:
            breastSide = b
            breast_or_volume = breast_or_volume.replace(b, "").strip()
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": "AddFeeding",
        "bottleOunces": "",
        "feedingMinutes": "",
        "breastSide": breastSide,
        "babyName" : "",
        "eventTime" : ""
    }


def add_sleep(spoken_text):
    note = spoken_text.replace("add note", "").strip()
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": "AddSleep",
        "hours" : "1",
        "minutes" : "20",
        "babyName" : "",
        "eventTime" : ""
    }


def add_weight(spoken_text):
    note = spoken_text.replace("add note", "").strip()
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": "AddWeight",
        "pounds" : "8",
        "ounces" : "6",
        "babyName" : "",
        "eventTime" : ""
    }


def add_note(spoken_text):
    note = spoken_text.replace("add note", "").strip()
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": "AddNote",
        "note": note,
        "babyName" : "",
        "eventTime" : ""
    }


def send_data_to_babystats(spoken_text):
    if spoken_text in single_event_text:
        newConditions = single_event(spoken_text)
    elif "add pumping" in spoken_text:
        newConditions = add_pumping(spoken_text)
    elif "add feeding" in spoken_text or "start feeding" in spoken_text or "end feeding" in spoken_text:
        newConditions = feeding(spoken_text)
    elif "add sleep" in spoken_text:
        newConditions = add_sleep(spoken_text)
    elif "add weight" in spoken_text:
        newConditions = add_weight(spoken_text)
    elif "add note" in spoken_text:
        newConditions = add_note(spoken_text)
    else:
        return {'statusMessage': "Sorry, I was not able to process your request."}
    params = json.dumps(newConditions).encode('utf8')
    req = urllib.request.Request(conditionsSetURL, data=params, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    response_text = response.read().decode('utf8')
    print(response_text)
    return json.loads(response_text)


if __name__ == "__main__":
    spoken_text = "add wet"
    send_data_to_babystats(spoken_text)

