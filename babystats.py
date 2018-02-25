import json
import urllib.request

myID = "1038505942"
myaccessToken = "2018-02-25:a02cf622-9ded-4bc6-ae30-846fcca363db"

conditionsSetURL = 'https://www.babystats.org/api/public'


def addwet():
    return {
        "id": myID,
        "accessToken": myaccessToken,
        "event": "AddWet",
        "babyName" : "",
        "eventTime" : ""
    }


def send_data_to_babystats(spoken_text):
    if spoken_text == "add wet":
        newConditions = addwet()
    params = json.dumps(newConditions).encode('utf8')
    req = urllib.request.Request(conditionsSetURL, data=params, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    response_text = response.read().decode('utf8')
    print(response_text)
    return json.loads(response_text)


if __name__ == "__main__":
    spoken_text = "add wet"
    send_data_to_babystats(spoken_text)

