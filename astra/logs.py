import time as t
from datetime import date
import getpass

def logs(what_command, Content):

    _OsUsername = getpass.getuser()
    _MainFolderDirectory = f"C:\\Users\\{_OsUsername}\\Appdata\\Local\\.astra\\"

    global logs_message
    time = t.localtime()
    current_time = t.strftime("[ %H:%M:%S ]", time)
    today = date.today()

    if what_command == "cls":
        logs_message = f"\n{today}; {current_time}; Action = CLS;"
    if what_command == "say":
        logs_message = f"\n{today}; {current_time}; Action = SAY; Content = \"{Content}\""
    if what_command == "status":
        logs_message = f"\n{today}; {current_time}; Action = STATUS;"
    if what_command == "chngname":
        logs_message = f"\n{today}; {current_time}; Action = CHNGNAME; ContentBefore = {Content[0]}; ContentAfter = {Content[1]};"
    if what_command == "time":
        logs_message = f"\n{today}; {current_time}; Action = TIME;"
    if what_command == "date":
        logs_message = f"\n{today}; {current_time}; Action = DATE;"
    if what_command == "log.clr":
        logs_message = f"\n{today}; {current_time}; Action = LOG.CLEAR;"
    if what_command == "log.size":
        logs_message = f"\n{today}; {current_time}; Action = LOG.SIZE;"
    if what_command == "pcinfo":
        logs_message = f"\n{today}; {current_time}; Action = PCINFO;"
    if what_command == "settheme":
        logs_message = f"\n{today}; {current_time}; Action = SETTHEME; ContentBefore = {Content[0]}; ContentAfter = {Content[1]};"
    if what_command == "vercheck.done.noUpdate":
        logs_message = f"\n{today}; {current_time}; Action = VERCHECK; VerStatus = LATEST"
    if what_command == "vercheck.done.needUpdate":
        logs_message = f"\n{today}; {current_time}; Action = VERCHECK; VerStatus = OUTDATED"
    if what_command == "vercheck.netwrokError":
        logs_message = f"\n{today}; {current_time}; Action = VERCHECK; VerStatus = ERROR; Error = NETWORK_ERROR"
    if what_command == "themes":
        logs_message = f"\n{today}; {current_time}; Action = THEMES;"
    if what_command == "help":
        logs_message = f"\n{today}; {current_time}; Action = HELP;"
    if what_command == "restart":
        logs_message = f"\n{today}; {current_time}; Action = RESTART;"
    if what_command == "testnet":
        logs_message = f"\n{today}; {current_time}; Action = TESTNET;"
    if what_command == "websearch":
        logs_message = f"\n{today}; {current_time}; Action = WEBSEARCH; Content = \"{Content}\""
    if what_command == "webopen":
        logs_message = f"\n{today}; {current_time}; Action = WEBOPEN; Url = "

    logsWrite = open(f"{_MainFolderDirectory}logs.txt", "a+")
    logsWrite.write(logs_message)
    logsWrite.close()
