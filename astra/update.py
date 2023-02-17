# That's not my code,  MADE BY: Zielin0

import os

updateScript = True
updateLibraries = True
libraries = ["bs4", "psutil", "GPUtil", "speedtest-cli"]
scriptRootURL = r"https://raw.githubusercontent.com/GentalYT/astra_console/main/"

cfg = {
    "astra.py" : {"URL" : "astra.py", "file" : "astra.py"},
    "help.py" : {"URL" : "help.py", "file" : "help.py"},
    "logs.py" : {"URL" : "logs.py", "file" : "logs.py"},
    "pcinfo.py" : {"URL" : "pcinfo.py", "file" : "pcinfo.py"}
}

if not "requests" in libraries:
    libraries.append("requests")

if updateLibraries:
    for i in libraries:
        os.system(f"pip install {i}")

import requests

if updateScript:
    for i in cfg:
        with open(cfg[i]["file"], "w") as f:
            f.write(requests.get(scriptRootURL + cfg[i]["URL"]).text)

import astra
