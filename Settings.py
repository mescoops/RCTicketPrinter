
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import json 

class Settings:
    
    url = "http://localhost:4432"
    data_json = None
    defaults = '''
{
"teams":["Tinkers", "Stichers", "Sharpies", "Jewlery", "Wood", "Garden"],
"location":{"name":"Pasadena", "date":""},
"printerMAC":"86:67:7A:8D:EB:63"
}
'''
    def __init__(self):
        global data_json
        try:
            response = urlopen(self.url) 
            self.data_json = json.loads(response.read()) 
        except URLError as err:
            self.data_json = json.loads(self.defaults) 
   
    def printerMAC(self):
        return self.data_json["printerMAC"]

    def locationName(self):
        return self.data_json["location"]["name"]
        
    def locationDate(self):
        return self.data_json["location"]["date"]

    def teams(self):
        return self.data_json["teams"]
