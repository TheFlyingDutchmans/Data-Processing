import requests
import json
import matplotlib.pyplot as plt
import folium

m = folium.Map(
    location=[34.825830, 18.359418],
    zoom_start=2,
    max_bounds=True,
    min_zoom=2,
    width='100%',
    height='100%'
)

url = "http://127.0.0.1:1234/api/getSpoofData"

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
    response = requests.request("GET", url, headers=headersJSON, data=getShipPayloadJSON)
    response_info = json.loads(response.text)
    return response_info


def getAllSpoofData():
    getSpoofDataPayloadJSON = json.dumps({
        "request": {
        },
        "user": {
            "apiKey": "admin"
        }
    })
    response = requests.request("GET", url, headers=headersJSON, data=getSpoofDataPayloadJSON)
    response_info = json.loads(response.text)
    return response_info


def getSingleSpoofData(id):
    getSpoofDataPayloadJSON = json.dumps({
        "request": {
            "spoofID": str(id)
        },
        "user": {
            "apiKey": "admin"
        }
    })
    response = requests.request("GET", url, headers=headersJSON, data=getSpoofDataPayloadJSON)
    response_info = json.loads(response.text)
    return response_info


def getDataForMap(id):
    response_info = getSingleSpoofData(id)
    spoof = response_info["spoofData"]
    lat = spoof["latitude"]
    long = spoof["longitude"]
    time = spoof["currentTime"]
    return lat, long, time


def displaySingleShip(id):
    lat, long, time = getDataForMap(id)
    folium.Marker(
        location=[lat, long],
        popup=str(time),
    ).add_to(m)


def displayAllShips():
    response_info = getAllSpoofData()
    for spoof in response_info['spoofData']:
        lat = spoof["latitude"]
        long = spoof["longitude"]
        time = spoof["currentTime"]
        folium.Marker(
            location=[lat, long],
            popup=str(time),
        ).add_to(m)


displaySingleShip(8)
m.save('map.html')
