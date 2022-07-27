import quantaq
import json
from . import quantaq_key
import os.path
from datetime import date
QUANTAQ_APIKEY = quantaq_key.QUANTAQ_APIKEY
client = quantaq.QuantAQAPIClient(api_key=QUANTAQ_APIKEY)

def list_sensors():
    devices_raw = client.devices.list(filter="city,like,%_oxbury%")
    return devices_raw

def get_location_device(device):
    lat = device['geo']['lat']
    lon = device['geo']['lon']
    return lat,lon

def document_device_features(devices_raw, filename):
    store = {}
    with open(filename,'w') as f:
        for device in devices_raw:
            if '\'' in device["description"]:
                device["description"] = device["description"].replace('\'','')
            store[device["id"]] = device

        f.write(json.dumps(store))

def read_document(filename):
    with open(filename,'r') as f:
        s = ''.join(f.readlines())
        store = json.loads(s)
        return store

def update_sensor_list(filename="sensor_list.json", devices_raw=list_sensors()):
    path = "./src/static/scripts/"
    full_path = os.path.join(path + filename)
    document_device_features(devices_raw, full_path)
    return read_document(full_path)

def get_sensor_ids():
    sns = {}
    devices_raw = client.devices.list(filter="city,like,Roxbury")
    for device in devices_raw:
        id = device["id"]
        sn = device["sn"]
        sns[id] = sn
    return sns

def append_sensor_data(data={}):
    sns = get_sensor_ids()
    for id in sns:
        data_raw = client.data.list(sn=sns[id], start=str(date.today()), sort="timestamp,asc", limit=1)
        
        # data_raw = client.data.bydate(sn=sns[id], date=str(date.today()), sort="timestamp,asc", limit=1)
        # data_raw = client.data.get(id=id, sn=sns[id])
        if len(data_raw) > 0:
            d = data_raw[0]
            data[id] = {'lat': d['geo']['lat'] if d['geo']['lat'] is not None else -1,
                        'lon': d['geo']['lon'] if d['geo']['lon'] is not None else -1,
                        'pm1': "Good" if d['pm1'] < 2 else "Okay" if d["pm1"] >= 2 and d['pm1'] < 5 else "Bad" if d['pm1'] >= 5 else "None",
                        'pm25': "Good" if d['pm25'] < 5 else "Okay" if d["pm25"] >= 5 and d['pm25'] < 12.5 else "Bad" if d['pm25'] >= 12.5 else "None",
                        'pm10': "Good" if d['pm1'] < 20 else "Okay" if d["pm1"] >= 20 and d['pm1'] < 35 else "Bad" if d['pm1'] >= 35 else "None"}

            if 'met' in d: # For compatibility with older sensors
                if d['met'] is not None:
                    data[id]['met'] = d['met']
                else:
                    data[id]['met'] = -1

# def plot_sensor_data(data, plots):
#     for id in data:

# if __name__ == "__main__":
#     # update_sensor_list()
#     # teams = client.teams.list()
#     # for i in range(len(teams)):
#     #     print(teams[i]['id'])
#     append_sensor_data()