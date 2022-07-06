import quantaq
import json
import quantaq_key
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
    with open(filename,'w') as f:
        for device in devices_raw:
            f.write(json.dumps(device))
            f.write('\n')

def read_document(filename, device_list={}): # For debugging purposes if the file needs to be printed out
    with open(filename,'r') as f:
        for line in f.readlines():
            line = json.loads(line)
            name = line["id"]
            device_list[name] = line
            print(line)

def update_sensor_list(filename="sensor_list.txt", devices_raw=list_sensors()):
    document_device_features(devices_raw, filename)
    read_document(filename)

if __name__ == "__main__":
    update_sensor_list()