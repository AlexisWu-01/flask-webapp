import quantaq
import json
from . import quantaq_key
import os.path
from datetime import date
QUANTAQ_APIKEY = quantaq_key.QUANTAQ_APIKEY
client = quantaq.ProductionAPIClient(api_key=QUANTAQ_APIKEY) # this line may need to be changed to a different client depending on quantaq

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

def get_sensor_ids(filter, sns={}):
    devices_raw = client.devices.list(filter=filter)
    for device in devices_raw:
        id = device["id"]
        sn = device["sn"]
        desc = device['description']
        sns[id] = [sn, desc]
    return sns

def append_sensor_data(data={}):
    sns = get_sensor_ids("city,like,Roxbury", {})
    sns = get_sensor_ids("city,like,East Boston", sns)
    for id in sns:
        data_raw = client.data.list(sn=sns[id][0], start=str(date.today()), sort="timestamp,asc", limit=1)
        
        if len(data_raw) > 0:
            d = data_raw[0]
            data[id] = {
                'lat': d['geo']['lat'] if d['geo']['lat'] is not None else -1,
                'lon': d['geo']['lon'] if d['geo']['lon'] is not None else -1,
                'pm1': evaluate_pm(d.get('pm1'), 2, 5),
                'pm25': evaluate_pm(d.get('pm25'), 5, 12.5),
                'pm10': evaluate_pm(d.get('pm10'), 20, 35),
                'desc': sns[id][1]
            }

            if 'met' in d:  # For compatibility with older sensors
                data[id]['met'] = d['met'] if d['met'] is not None else -1

def evaluate_pm(value, threshold_okay, threshold_bad):
    if value is None:
        return "None"
    elif value < threshold_okay:
        return [value, "Good", "green"]
    elif threshold_okay <= value < threshold_bad:
        return [value, "Okay", "yellow"]
    else:
        return [value, "Bad", "red"]



# def plot_sensor_data(data, plots):
#     for id in data:

# if __name__ == "__main__":
#     # update_sensor_list()
#     # teams = client.teams.list()
#     # for i in range(len(teams)):
#     #     print(teams[i]['id'])
#     append_sensor_data()
    