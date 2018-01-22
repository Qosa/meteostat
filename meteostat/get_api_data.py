import requests
import json
from urllib2 import urlopen

def getIpData():
    url = 'http://ip-api.com/json'
    response = urlopen(url)
    data = json.load(response)
    return data

def getOWMData():
    api = requests.get("http://api.openweathermap.org/data/2.5/weather?lat="+str(getIpData()['lat'])+"&lon="+str(getIpData()['lon'])+"&appid=7eba99ded11d5b65905e36749ac8e398")
    api_data = api.json()
    return api_data

