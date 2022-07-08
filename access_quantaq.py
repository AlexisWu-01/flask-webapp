import quantaq
import json
import quantaq_key
import os.path
from quantaq.utils import to_dataframe
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
        for k,v in store.items():
            print(k, ":", v)
        return store

def update_sensor_list(filename="sensor_list.json", devices_raw=list_sensors()):
    path = "static/scripts/"
    full_path = os.path.join(path + filename)
    document_device_features(devices_raw, full_path)
    return read_document(full_path)

def append_sensor_data(data={}):
    sns = get_sensor_ids()
    print(sns)
    for id in sns:
        data_raw = client.data.get(id=id, sn=sns[id])
        print(data_raw)

def get_sensor_ids():
    sns = {}
    devices_raw = client.devices.list(filter="city,like,%_oxbury%")
    for device in devices_raw:
        id = device["id"]
        sn = device["sn"]
        sns[id] = sn
    return sns

if __name__ == "__main__":
    # update_sensor_list()
    append_sensor_data()