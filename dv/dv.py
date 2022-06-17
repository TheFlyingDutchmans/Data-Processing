import requests
import json
import matplotlib.pyplot as plt
import xmltodict as xmltodict
from Tools.scripts.parse_html5_entities import get_json
from matplotlib import animation

url = "http://127.0.0.1:1234/api/getShip"

payloadJSON = json.dumps({
    "ship": {},
    "user": {
        "apiKey": "admin"
    }
})
headersJSON = {
    'Content-Type': 'application/json'
}

payloadXML = "<root>\r\n    <ship>\r\n        <shipID>2</shipID>\r\n    </ship>\r\n    <user>\r\n        " \
             "<apiKey>admin</apiKey>\r\n    </user>\r\n</root>\r\n "
headersXML = {
    'Content-Type': 'application/xml'
}


def isJSON(check):
    try:
        json.loads(check)
    except ValueError as e:
        return False
    return True


def getData():
    response = requests.request("GET", url, headers=headersJSON, data=payloadJSON)
    if isJSON(response.text):
        response_info = json.loads(response.text)
    else:
        response = requests.request("GET", url, headers=headersXML, data=payloadXML)
        response_info = xmltodict.parse(response)
        response_info = response_info.popitem()[1]
    return response_info


def dataIntoArrays():
    mmsis = []
    response_info = getData()
    for ship in response_info['ships']:
        three = str(ship['mmsi'])[0:3]
        mmsis.append(three)

    dictOfCounts = {item: mmsis.count(item) for item in mmsis}
    dictOfCounts = dict(sorted(dictOfCounts.items(), key=lambda x: x[1], reverse=True))

    count = []
    values = []
    labels = []

    for i in range(len(dictOfCounts)):
        count.append(i)

    for item in dictOfCounts:
        values.append(dictOfCounts.get(item))
        labels.append(item)
    return count, values, labels


fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

count, values, labels = dataIntoArrays()
valuesAbr = []
labelsAbr = []
for i in range(10):
    valuesAbr.append(values[i])
    values.pop(i)
    labelsAbr.append(labels[i])

# labelsAbr.append("Other")
sum = 0
for i in values:
    sum += i
# valuesAbr.append(sum)

ax1.clear()
ax1.bar(labelsAbr, valuesAbr)

plt.show()
