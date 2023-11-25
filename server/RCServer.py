#!/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json 
import time
import pathlib

settingsFile = "rc.settings"

serverPort = 4432
settingsData = ""
settingsLastModified = None


class MyServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(getLastestData()), "utf-8"))

        
def getLastestData():
    global settingsData
    if settingsFileModified():
        with open(settingsFile, "r") as read_file:
            settingsData = json.load(read_file)
        print("Settings updated")
    return settingsData

    
def settingsFileModified():
    global settingsLastModified
    fPath = pathlib.Path(settingsFile)
    modified = settingsLastModified is None or settingsLastModified != fPath.stat().st_mtime
    settingsLastModified = fPath.stat().st_mtime
    return modified
        

#        self.wfile.write(bytes('''
#{
#"teams":["Tinkers", "Stichers", "Sharpies", "Jewlery", "Wood", "Glue", "Garden"],
#"location":{"name":"Side Street Projects", "date":"21 October 2023"}
#}
#''', "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer(("", serverPort), MyServer)
    print("Server started on port %s" % (serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
