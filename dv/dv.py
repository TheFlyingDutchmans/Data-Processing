import requests
import json
import folium

json_map = folium.Map(
    location=[34.825830, 18.359418],
    zoom_start=2,
    max_bounds=True,
    min_zoom=2,
    width='100%',
    height='100%'
)

xml_map = folium.Map(
    location=[34.825830, 18.359418],
    zoom_start=2,
    max_bounds=True,
    min_zoom=2,
    width='100%',
    height='100%'
)

url = "http://127.0.0.1:1234/api/getSpoofData"

headers_json = {
    'Content-Type': 'application/json'
}

headers_xml = {
    'Content-Type': 'application/xml'
}

def getAllSpoofData():
    get_spoof_data_payload_xml = "<root>\r\n    " \
                                    "<request></request>\r\n    " \
                                    "<user>\r\n        " \
                                        "<apiKey>admin</apiKey>\r\n    " \
                                    "</user>\r\n" \
                                 "</root>\r\n "
    response_xml = requests.request("GET", url, headers=headers_xml, data=get_spoof_data_payload_xml)
    response_info_xml = response_xml

    get_spoof_data_payload_json = json.dumps({
        "request": {
        },
        "user": {
            "apiKey": "admin"
        }
    })
    response_json = requests.request("GET", url, headers=headers_json, data=get_spoof_data_payload_json)
    response_info_json = json.loads(response_json.text)
    print(response_info_json)
    return response_info_json, response_info_xml


def getSingleSpoofData(id):
    get_spoof_data_payload_xml = "<root>\r\n    " \
                                    "<request>" + str(id) + "</request>\r\n    " \
                                    "<user>\r\n        " \
                                        "<apiKey>admin</apiKey>\r\n    " \
                                    "</user>\r\n" \
                                 "</root>\r\n "
    response_xml = requests.request("GET", url, headers=headers_xml, data=get_spoof_data_payload_xml)
    response_info_xml = response_xml

    get_spoof_data_payload_json = json.dumps({
        "request": {
            "spoofID": str(id)
        },
        "user": {
            "apiKey": "admin"
        }
    })
    response_json = requests.request("GET", url, headers=headers_json, data=get_spoof_data_payload_json)
    response_info_json = json.loads(response_json.text)

    return response_info_json, response_info_xml

def displaySingleShip(id):
    response_info_json, response_info_xml = getSingleSpoofData(id)
    addMarker(response_info_json["spoofData"], json_map)
    #addMarker(response_info_xml, xml_map)


def displayAllShips():
    response_info_json, response_info_xml = getAllSpoofData()
    for spoof in response_info_json["spoofData"]:
        addMarker(spoof, json_map)
    #addMarker(response_info_xml, xml_map)



def addMarker(spoof, m):
    print(spoof)
    lat = spoof["latitude"]
    long = spoof["longitude"]
    time = spoof["currentTime"]
    folium.Marker(
        location=[lat, long],
        popup=str(time),
    ).add_to(m)

displayAllShips()
displaySingleShip(10)
json_map.save('json_map.html')
xml_map.save('xml_map.html')
