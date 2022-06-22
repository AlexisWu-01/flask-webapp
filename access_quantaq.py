import quantaq
import ConfigParser
from quantaq.utils import to_dataframe
config = ConfigParser.ConfigParser()
config.read("config.ini")
QUANTAQ_APIKEY = config.get("quantaq_key", "QUANTAQ_APIKEY")
client = quantaq.QuantAQAPIClient(api_key=QUANTAQ_APIKEY)



def list_sensors():
    devices_raw = to_dataframe(client.devices.list(filter="city,like,%_oxbury%"))
    devices_simplified = devices_raw.iloc[:,[4,3,11,15,16,5,7,8,10,12]]
    return devices_simplified,devices_raw

def document_list(devices_raw, filename):
    with open(filename) as f:
        for device in devices_raw:
            f.write(device)

def print_document(filename): # For debugging purposes if the file needs to be printed out
    with open(filename) as f:
        for line in f.readlines():
            print(line)

if __name__ == "__main__":
    filename = "sensor_list.txt"
    devices_simplified, devices_raw = list_sensors()
    document_list(devices_raw, filename)
    print_document(filename)