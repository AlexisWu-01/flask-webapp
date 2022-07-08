import threading
import requests

def reloadapi():
    threading.Timer(5.0, reloadapi).start()
    r2 = requests.get(' http://api.adviceslip.com/advice')
    advice_result= r2.json()
    return advice_result