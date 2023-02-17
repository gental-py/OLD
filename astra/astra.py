_NotInstalledLibaries_List = []

from time import strftime
from datetime import date
import getpass as gp
from help import *
import time as t
import speedtest
import platform
import os

try:
    import requests
except ModuleNotFoundError:
    os.system("pip install requests")
    _NotInstalledLibaries_List.append("REQUESTS")
    import requests

try:
    import psutil
except ModuleNotFoundError:
    os.system("pip install PSUtil")
    _NotInstalledLibaries_List.append("PSUTIL")
    import psutil

try:
    import GPUtil
except ModuleNotFoundError:
    os.system("pip install GPUtil")
    _NotInstalledLibaries_List.append("GPUTIL")
    import GPUtil

try:
    import webbrowser
except ModuleNotFoundError:
    os.system("pip install webbrowser")
    _NotInstalledLibaries_List.append("WEBBROWSER")
    import webbrowser

try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    os.system("pip install bs4")
    _NotInstalledLibaries_List.append("BS4")
    from bs4 import BeautifulSoup

# TO DO:

# ----- = PRE VARS = ----- #
_OsUsername = gp.getuser()
_Version = "1.2"
_Mode = "dev"

# ----- = Colors = ----- #
BROWN = "\033[0;33m"
PURPLE = "\033[0;35m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BLUE = "\033[0;34m"
CYAN = "\033[0;36m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
END = "\033[0m"

# ------ = FILES = ------ #
OcupiedFiles_List = []
_MainFolderDirectory = f"C:\\Users\\{_OsUsername}\\Appdata\\Local\\.astra\\"

# ===[ Main Folder ]=== #
if not os.path.exists(f"C:/Users/{_OsUsername}/Appdata/Local/.astra/"):
    OcupiedFiles_List.append(1)
    Files_MainFolder_Directory = f"C:/Users/{_OsUsername}/Appdata/Local/"
    Files_MainFolder_Path = os.path.join(Files_MainFolder_Directory, ".astra")
    os.mkdir(Files_MainFolder_Path)
else:
    OcupiedFiles_List.append(0)

# ===[ Name File] === #
if not os.path.exists(f"C:/Users/{_OsUsername}/Appdata/Local/.astra/name.txt"):
    OcupiedFiles_List.append(1)
    open(f"{_MainFolderDirectory}name.txt", "a+")
else:
    OcupiedFiles_List.append(0)

# ===[ Logs File ]=== #
if not os.path.exists(f"C:/Users/{_OsUsername}/Appdata/Local/.astra/logs.txt"):
    OcupiedFiles_List.append(1)
    open(f"{_MainFolderDirectory}logs.txt", "a+")
else:
    OcupiedFiles_List.append(0)

# ===[ Theme File ]=== #
if not os.path.exists(f"C:/Users/{_OsUsername}/Appdata/Local/.astra/theme.txt"):
    OcupiedFiles_List.append(1)
    open(f"{_MainFolderDirectory}theme.txt", "a+")
    settheme_File_w = open(f"{_MainFolderDirectory}theme.txt", "w+")
    settheme_File_w.write("arctic")
    settheme_File_w.close()
else:
    OcupiedFiles_List.append(0)

# ===[ Repair colors in console ]=== #
if not __import__("sys").stdout.isatty():
    for _ in dir():
        if isinstance(_, str) and _[0] != "_":
            locals()[_] = ""
else:
    if __import__("platform").system() == "Windows":
        kernel32 = __import__("ctypes").windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32

class PreMessage:
    error = f"{LIGHT_BLUE}[{RED}!{LIGHT_BLUE}]{END}"
    notification = f"{LIGHT_BLUE}[{LIGHT_RED}*{LIGHT_BLUE}]{END}"
    column = f"{LIGHT_BLUE}[{LIGHT_RED}-{LIGHT_BLUE}]{END}"

# ----- = Name = ----- #
name_File_R = open(f"{_MainFolderDirectory}name.txt", "r")
if os.path.getsize(f"{_MainFolderDirectory}name.txt") == 0:
    while True:
        name_NewName_Input = input("[?] Username: ")

        if len(name_NewName_Input) > 20:
            print(f"{CYAN}[{LIGHT_RED}!{CYAN}] {LIGHT_PURPLE}Username cannot be longer than 20 chars!")
        else:
            print(f"{CYAN}[{YELLOW}*{CYAN}] {LIGHT_PURPLE}Sucessfully setted name to: {name_NewName_Input}")
            _Name = name_NewName_Input
            name_File_W = open(f"{_MainFolderDirectory}name.txt", "w+")
            name_File_W.write(_Name)
            name_File_W.close()
            break
else:
    _Name = name_File_R.read()

# ----- = Themes = ----- #
theme_File_R = open(f"{_MainFolderDirectory}theme.txt", "r")
theme_File_R = theme_File_R.read()

if theme_File_R == "arctic":
    _Theme = "arctic"

elif theme_File_R == "sunset":
    _Theme = "sunset"

elif theme_File_R == "pinked":
    _Theme = "pinked"

elif theme_File_R == "light":
    _Theme = "light"

else:
    _Theme = "arctic"
    settheme_File_w = open(f"{_MainFolderDirectory}theme.txt", "w+")
    settheme_File_w.write("arctic")
    settheme_File_w.close()

# ----- = Functions = ----- #
def cls():
    os.system("cls")

def listToString(listToConv):
    str1 = ""
    for ele in listToConv:
        str1 += ele
    return str1

# ----- = PRE ACTIONS = ----- #
os.system("cls")

if len(_NotInstalledLibaries_List) > 0:
    print(f"{RED}* {GREEN}Installed missing libaries: {LIGHT_RED}{listToString(_NotInstalledLibaries_List)}")

# ----- = MAIN LOOP = ----- #
while True:
    # += Import logs libary. =+ #
    from logs import *

    # += Check for name updates. =+ #
    name_File_R = open(f"{_MainFolderDirectory}name.txt", "r")
    _Name = name_File_R.read()

    # += Themes Class. =+ #
    class Themes:
        arctic = f"{LIGHT_CYAN}${CYAN}{_Name}{LIGHT_CYAN}.{CYAN}{_Mode}{LIGHT_CYAN}>{WHITE}"
        sunset = f"{LIGHT_PURPLE}${BROWN}{_Name}{YELLOW}.{BROWN}{_Mode}{LIGHT_PURPLE}>{YELLOW}"
        pinked = f"{LIGHT_PURPLE}${PURPLE}{_Name}{LIGHT_PURPLE}.{PURPLE}{_Mode}{LIGHT_CYAN}>{LIGHT_RED}"
        light  = f"{YELLOW}${WHITE}{_Name}{YELLOW}.{WHITE}{_Mode}{YELLOW}>{WHITE}"

    # += Set theme for input. =+ #
    try:
        if _Theme == "arctic":
            _Command = input(f"{Themes.arctic}")
        if _Theme == "sunset":
            _Command = input(f"{Themes.sunset}")
        if _Theme == "pinked":
            _Command = input(f"{Themes.pinked}")
        if _Theme == "light":
            _Command = input(f"{Themes.light}")
    except KeyboardInterrupt:
        continue

    # += Convert input to list. =+ #
    _ListedCommand_Lower = list(_Command.lower())
    _ListedCommand = list(_Command)

    # += Check for errors =+ #
    if _ListedCommand_Lower == []:
        continue
    else:
        while True:
            if _ListedCommand_Lower[0] == " ":
                _ListedCommand_Lower.pop(0)
            else:
                break

    # ----- = Commands = ----- #

    #   [ EXIT ]   #
    if _Command.lower().startswith("exit"):
        print(END)
        exit()

    #   [ HELP ]   #
    if _Command.lower().startswith("help"):
        help()
        logs("help", None)

    #   [ RESTART ]   #
    if _Command.lower().startswith("restart"):
        os.system("py astra.py")
        logs("restart", None)

    #   [ SAY ]   #
    if _Command.lower().startswith("say"):

        for i in range(3):
            _ListedCommand.pop(0)
        try:
            if _ListedCommand[0] == " ":
                _ListedCommand.pop(0)
        except IndexError:
            pass

        if "--a" in _Command:
            for i in range(len(_ListedCommand)):
                if _ListedCommand[i] == "-":
                    if _ListedCommand[i + 1] == "-":
                        try:
                            if _ListedCommand[i + 2] == "a":
                                say_AsayPrefix_location = i
                        except IndexError:
                            pass

            for i in range(3):
                _ListedCommand.pop(say_AsayPrefix_location)

            while True:
                if _ListedCommand[0] == " ":
                    _ListedCommand.pop(0)
                else:
                    break

            print(*_ListedCommand)
        else:
            print(*_ListedCommand, sep="")

        logs_Content = listToString(_ListedCommand)
        logs("say", logs_Content)

    #   [ CLS ]   #
    if _Command.lower().startswith("cls"):
        cls()
        logs("cls", None)

    #   [ STATUS ]   #
    if _Command.lower().startswith("status"):
        status_NameFile_size = str(int(os.path.getsize(f"{_MainFolderDirectory}name.txt") / 8)) + " Kb"
        status_LogsFile_size = str(int(os.path.getsize(f"{_MainFolderDirectory}logs.txt") / 8)) + " Kb"
        status_ThemeFile_size = str(int(os.path.getsize(f"{_MainFolderDirectory}theme.txt") / 8)) + " Kb"
        status_MainFile_size = str(int(os.path.getsize("astra.py") / 8)) + " Kb"
        status_Modules_Help_size = str(int(os.path.getsize(f"{_MainFolderDirectory}help.py") / 8)) + " Kb"
        status_Modules_Pcinfo_size = str(int(os.path.getsize(f"{_MainFolderDirectory}pcinfo.py") / 8)) + " Kb"
        status_Modules_Logs_size = str(int(os.path.getsize(f"{_MainFolderDirectory}logs.py") / 8)) + " Kb"
        sizes_list = [f"\n{YELLOW}.Txt\n{BLUE}   > Name:{LIGHT_RED} ",status_NameFile_size, f"\n{BLUE}   > Logs:{LIGHT_RED} ", status_LogsFile_size, f"\n{BLUE}   > Theme:{LIGHT_RED} ", status_ThemeFile_size, f"\n{YELLOW}.Py\n{BLUE}   > Main:{LIGHT_RED} ", status_MainFile_size, f"\n{BLUE}   > Help:{LIGHT_RED} ", status_Modules_Help_size, f"\n{BLUE}   > Pcinfo:{LIGHT_RED} ", status_Modules_Pcinfo_size, f"\n{BLUE}   > Logs:{LIGHT_RED} ", status_Modules_Logs_size, "\n"]
        print(f"{PreMessage.column} {CYAN}Startup = {LIGHT_RED}", *OcupiedFiles_List,
              f"\n{PreMessage.column} {CYAN}Sizes   = {LIGHT_RED}", *sizes_list,
              f"\n{PreMessage.column} {CYAN}Version = {LIGHT_RED}",
              _Version + f"\n{PreMessage.column} {CYAN}Name    = {LIGHT_RED}", _Name, sep="")

        logs("status", None)

    #   [ CHNGNAME ]   #
    if _Command.lower().startswith("chngname"):

        chngname_Mode = bool
        logs_chngname_contentBefore = _Name

        # [Convert command an choose mode]
        for i in range(8):
            _ListedCommand.pop(0)

        while True:
            try:
                if _ListedCommand[0] == " ":
                    _ListedCommand.pop(0)
                else:
                    break
            except IndexError:
                break

        if listToString(_ListedCommand) == "":
            chngname_Mode = False
        else:
            chngname_Mode = True
            chngname_NewName = listToString(_ListedCommand)

        if chngname_Mode == False:
            while True:
                cls()
                chngname_NewName = input(f"{LIGHT_CYAN}${CYAN}New name{LIGHT_CYAN}>{WHITE}")
                if len(chngname_NewName) > 20:
                    print(f"{PreMessage.error} {LIGHT_RED}Name cannot be longer than 20 characters!")
                    t.sleep(2)
                    continue
                else:
                    name_File_W = open(f"{_MainFolderDirectory}name.txt", "w+")
                    name_File_W.write(chngname_NewName)
                    name_File_W.close()
                    print(f"{PreMessage.notification} {LIGHT_GREEN}Name has been updated to:", chngname_NewName)
                    break
        else:
            if len(chngname_NewName) > 20:
                print(f"{PreMessage.error} {LIGHT_RED}Name cannot be longer than 20 characters!")
                t.sleep(2)
                continue
            else:
                name_File_W = open(f"{_MainFolderDirectory}name.txt", "w+")
                name_File_W.write(chngname_NewName)
                name_File_W.close()
                print(f"{PreMessage.notification} {LIGHT_GREEN}Name has been updated to:", chngname_NewName)

        logs_chngname_content = (logs_chngname_contentBefore, chngname_NewName)

        logs("chngname", logs_chngname_content)

    #   [ TIME ]   #
    if _Command.lower().startswith("time"):
        time_LocalTime = t.localtime()
        time_CurrentTime = strftime(f" {LIGHT_CYAN}[ {CYAN}%H:%M:%S {LIGHT_CYAN}]", time_LocalTime)
        print(time_CurrentTime)
        logs("time", None)

    #   [ DATE ]   #
    if _Command.lower().startswith("date"):
        date_Today = date.today()
        print(f" {LIGHT_CYAN}[ {CYAN}{date_Today}{LIGHT_CYAN} ]")
        logs("date", None)

    #   [ LOG ]   #
    if _Command.lower().startswith("log"):
        log_status_LogsFile_size = os.path.getsize(f"{_MainFolderDirectory}logs.txt")
        if "-clr" in _Command.lower():
            open(f"{_MainFolderDirectory}logs.txt", 'w').close()
            print(f"{PreMessage.notification} {LIGHT_GREEN}Cleared {GREEN}{log_status_LogsFile_size} B {LIGHT_GREEN}of memory!")
            logs("log.clr", None)

        if "-size" in _Command.lower():
            print(f"{PreMessage.notification} {LIGHT_GREEN}Size: {GREEN}{log_status_LogsFile_size} B")
            logs("log.size", None)

        if "-show" in _Command.lower():
            log_ReadFile = open(f"{_MainFolderDirectory}logs.txt", "r")
            log_Read = log_ReadFile.read()
            print(LIGHT_BLUE)
            print(log_Read)

        if "-size" not in _Command.lower() and "-clr" not in _Command.lower() and "-show" not in _Command.lower():
            print(f"{PreMessage.error} {LIGHT_RED}Add {RED}-clr {LIGHT_RED}or {RED}-size {LIGHT_RED}or {RED}-show {LIGHT_RED}to command!")

    #   [ TESTNET ]   #
    if _Command.lower().startswith("testnet"):

        testnet_st = speedtest.Speedtest()
        print(f"{PreMessage.notification}{GREEN}Connected to server. Checking...")
        testnet_download = int(testnet_st.download())/1024/1024
        testnet_upload = int(testnet_st.upload())/1024/1024
        testnet_ping = testnet_st.results.ping
        print(f"{PreMessage.column}{CYAN}Download: {LIGHT_BLUE}{int(testnet_download)} Mb/s")
        print(f"{PreMessage.column}{CYAN}Upload: {LIGHT_BLUE}{int(testnet_upload)} Mb/s")
        print(f"{PreMessage.column}{CYAN}Ping: {LIGHT_BLUE}{int(testnet_ping)}")
        logs("testnet", None)

    #   [ PCINFO ]   #
    if _Command.lower().startswith("pcinfo"):
        from pcinfo import *
        pcinfo(_Command)
        logs("pcinfo", None)

    #   [ VERCHECK ]   #
    if _Command.lower().startswith("vercheck"):
        # ----- = Check for updates = ----- #
        try:
            checkForUpdates_VersionURL = "https://raw.githubusercontent.com/GentalYT/astra_console/main/README.md"
            checkForUpdates_HtmlCode = requests.get(checkForUpdates_VersionURL)
            checkForUpdates_BS4soup = BeautifulSoup(checkForUpdates_HtmlCode.text, 'html.parser')
            checkForUpdates_NewVersion = checkForUpdates_BS4soup

            # Check
            if str(checkForUpdates_NewVersion) == _Version + "\n":
                print(f"{PreMessage.notification} {LIGHT_GREEN}Program have newest version.")
                logs("vercheck.done.noUpdate", None)
            else:
                print(f"{PreMessage.error} {LIGHT_RED}Hey! You have outdated version! Donwload newest from:\n{RED}{PreMessage.column} https://github.com/GentalYT/astra_console")
                logs("vercheck.done.needUpdate", None)
                print(f"{PreMessage.notification}{GREEN}Do you want to auto update program? (y/n)")
                vercheck_AskForUpdate = input(f"{LIGHT_GREEN} >")
                while vercheck_AskForUpdate.lower() not in ("y", "n"):
                    print(f"{PreMessage.error}{RED}Type Y or N")
                    vercheck_AskForUpdate = input(f"{LIGHT_GREEN} >")

                if vercheck_AskForUpdate.lower() == "y":
                    import update
                    print(f"{GREEN}* {LIGHT_GREEN}Wait...")


        except requests.exceptions.ConnectionError:
            print(f"{PreMessage.error} {LIGHT_RED} You do not have internet connection!")
            logs("vercheck.netwrokError", None)

    #   [ THEMES ]   #
    if _Command.lower().startswith("themes"):
        print(f"\n{LIGHT_CYAN}Arc{CYAN}tic: {Themes.arctic}")
        print(f"{BROWN}Sun{LIGHT_PURPLE}set: {Themes.sunset}")
        print(f"{LIGHT_PURPLE}Pinked: {Themes.pinked}")
        print(f"{WHITE}Light{YELLOW}:  {Themes.light}\n")
        print(f"{PreMessage.notification} {LIGHT_GREEN} Type \"settheme <name>\" to set one of them!")
        logs("themes", None)

    #   [ SETTHEME ]   #
    if _Command.lower().startswith("settheme"):

        settheme_inCommand_arctic = False
        settheme_inCommand_sunset = False
        settheme_inCommand_pinked = False
        settheme_inCommand_light  = False

        settheme_typedThemes_list = []
        if "arctic" in _Command.lower():
            settheme_inCommand_arctic = True
            settheme_typedThemes_list.append("arctic")

        if "sunset" in _Command.lower():
            settheme_inCommand_sunset = True
            settheme_typedThemes_list.append("sunset")

        if "pinked" in _Command.lower():
            settheme_inCommand_pinked = True
            settheme_typedThemes_list.append("pinked")

        if "light" in _Command.lower():
            settheme_inCommand_light = True
            settheme_typedThemes_list.append("light")

        if len(settheme_typedThemes_list) == 1:

            logs_settheme_before = _Theme

            settheme_write = open(f"{_MainFolderDirectory}theme.txt", "w+")

            if settheme_inCommand_arctic == True:
                _Theme = "arctic"
                settheme_write.write("arctic")
                settheme_write.close()

            if settheme_inCommand_sunset == True:
                _Theme = "sunset"
                settheme_write.write("sunset")
                settheme_write.close()

            if settheme_inCommand_pinked == True:
                _Theme = "pinked"
                settheme_write.write("pinked")
                settheme_write.close()

            if settheme_inCommand_light == True:
                _Theme = "light"
                settheme_write.write("light")
                settheme_write.close()

            settheme_typedThemes_list.clear()

            settheme_logs_content = (logs_settheme_before, _Theme)
            logs("settheme", settheme_logs_content)

        else:
            print(f"{PreMessage.error} {LIGHT_RED}You have typed command uncorrect!")
            settheme_typedThemes_list.clear()

    #   [ WEBSEARCH ]   #
    if _Command.lower().startswith("websearch"):
        # Convert command
        try:
            for i in range(9):
                _ListedCommand_Lower.pop(0)
        except IndexError:
            print(f"{PreMessage.error}{RED}Web command syntax: {LIGHT_RED}web search/open phrase/link{RED} !")

        if _ListedCommand_Lower[0] == " ":
            _ListedCommand_Lower.pop(0)

        websearch_phrase = listToString(_ListedCommand_Lower)
        websearch_LogsContent = websearch_phrase

        websearch_phrase = websearch_phrase.replace(" ", "+")
        websearch_google = "https://www.google.com/search?q="

        websearch_ready = websearch_google + websearch_phrase
        webbrowser.open_new(websearch_ready)
        logs("websearch", websearch_LogsContent)

    #   [ WEBOPEN ]   #
    if _Command.lower().startswith("webopen"):
        try:
            for i in range(7):
                _ListedCommand_Lower.pop(0)
        except IndexError:
            print(f"{PreMessage.error}{RED}Web command syntax: {LIGHT_RED}web search/open phrase/link{RED} !")

        try:
            while True:
                if _ListedCommand_Lower[0] == " ":
                    _ListedCommand_Lower.pop(0)
                else:
                    break
            if len(_ListedCommand_Lower) > 3:
                webopen_url = listToString(_ListedCommand_Lower)
            else:
                print(f"{PreMessage.error}{RED}Error: invalid command! Try type {LIGHT_RED}<help>{RED} to show all commands!")

            webbrowser.open_new(webopen_url)

        except IndexError:
            print(f"{PreMessage.error}{RED}Web command syntax: {LIGHT_RED}web search/open phrase/link{RED} !")
