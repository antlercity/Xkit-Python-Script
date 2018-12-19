# script that queries the Sigfox backend using an API Access
# written in Python 3.6

# script to decript the sens'it payload for temperature
import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime

def main():
    # Sigfox API
    user = '5b038c8f50057408b4aa9b17'
    password = 'af854be331920bfa3225102d7aa77949'

    # Xkit Device ID
    deviceId = '3FB04C'

    url = 'https://backend.sigfox.com/api/devices/' + str(deviceId) +'/messages?limit=5'

    # API json information
    r = requests.get(url, auth=HTTPBasicAuth(user, password))
    # print(r.status_code)
    # print(r.text)

    json_text = json.loads(r.text)

    print('Device ID :',json_text["data"][0]["device"])
    #print('Time payload :',json_text["data"][0]["time"])
    ts = int(json_text["data"][0]["time"])

    print('Time sent :',datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    print('payload data :',json_text["data"][0]["data"])

    #store payload bytes into list
    payload = [json_text["data"][0]["data"][0:2]]
    i = 2
    j = 4
    while i < 23:
        payload.append(json_text["data"][0]["data"][i:j])
        i = i + 2
        j = j + 2

    #create list of raw sensor readings + convert hex values to decimal
    int_values = [int(payload[1]+payload[0],16)]
    i = 2
    while i < 11:
        int_values.append(int(payload[i+1]+payload[i],16))
        i += 2

    print('Temperature :',int_values[0] / float(100),'deg C')
    print('Pressure :',int_values[1] * float(3),'Pa')
    print('Photo :',int_values[2] / float(1000),'V')
    print('X_Acc :',int_values[3] / float(250),'g')
    print('X_Acc :',int_values[4] / float(250),'g')
    print('X_Acc :',int_values[5] / float(250),'g')

if __name__== "__main__":
    main()