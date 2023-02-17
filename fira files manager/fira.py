# chnglog: Show if admin on banner. Update. Download missing libaries.

class Program:
    version = 0.9


# Check if libaries are installed.
import os
try: import prompt_toolikt
except: os.system("pip install prompt_toolkit")

try: import configparser
except: os.system("pip install configparser")

try: import requests
except: os.system("pip install requests")

# Import libaries.
from prompt_toolkit.completion import NestedCompleter, WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.formatted_text import HTML
from datetime import datetime
import configparser as cp
import getpass as gp
import requests as r
import platform
import fnmatch
import shutil
import ctypes
import sys
import re


# Check if running on Windows.
if platform.system() != "Windows":
    print(f"You are not running FiraFiles {Program.version} on Windows.")
    exit()


# Minor functions.
def WaitForEnter():
    print(bold)
    os.system('pause')
    print(end)

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def cls(): 
    os.system("cls || clear")

def argParse(string):
    rv = []
    for match in re.finditer(r"('([^'\\]*(?:\\.[^'\\]*)*)'"
                             r'|"([^"\\]*(?:\\.[^"\\]*)*)"'
                             r'|\S+)\s*', string, re.S):
        arg = match.group().strip()
        if arg[:1] == arg[-1:] and arg[:1] in '"\'':
            arg = arg[1:-1].encode('ascii', 'backslashreplace') \
                .decode('unicode-escape')
        try:
            arg = type(string)(arg)
        except UnicodeError:
            pass
        rv.append(arg)
    return rv


# Colors.
if not sys.stdout.isatty():
    for _ in dir():
        if isinstance(_, str) and _[0] != "_":
            locals()[_] = ""
else:
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    del kernel32

underline = "\033[4m"
crossed = "\033[9m"
orange = "\033[0;33m"
purple = "\033[1;35m"
green = "\033[1;32m"
blink = "\033[5m"
bold = "\033[1;37m"
blue = "\033[1;34m"
gray = "\033[1;30m"
cyan = "\033[1;36m"
red = "\033[1;31m"
end = "\033[0m"


# Menus.
def DrawBanner():
    cls()
    if Configuration.showBanner:
        print(f"""{red}⠀⠀⠀⠀⠀⠀⢱⣆⠀⠀⠀⠀⠀⠀ {orange}\n{red}⠀⠀⠀⠀⠀⠀⠈⣿⣷⡀⠀⠀⠀⠀ {orange}                           \n{red}⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣧⠀⠀⠀ {orange}                             \n{red}⠀⠀⠀⠀⡀⢠⣿⡟⣿⣿⣿⡇⠀⠀ {orange}     ███████╗██╗██████╗░░█████╗░███████╗██╗██╗░░░░░███████╗░██████╗\n{red}⠀⠀⠀⠀⣳⣼⣿⡏⢸⣿⣿⣿⢀⠀ {orange}     ██╔════╝██║██╔══██╗██╔══██╗██╔════╝██║██║░░░░░██╔════╝██╔════╝\n{red}⠀⠀⠀⣰⣿⣿⡿⠁⢸⣿⣿⡟⣼⡆ {orange}     █████╗░░██║██████╔╝███████║█████╗░░██║██║░░░░░█████╗░░╚█████╗░\n{red}⢰⢀⣾⣿⣿⠟⠀⠀⣾⢿⣿⣿⣿⣿ {orange}     ██╔══╝░░██║██╔══██╗██╔══██║██╔══╝░░██║██║░░░░░██╔══╝░░░╚═══██╗\n{red}⢸⣿⣿⣿⡏⠀⠀⠀⠃⠸⣿⣿⣿⡿ {orange}     ██║░░░░░██║██║░░██║██║░░██║██║░░░░░██║███████╗███████╗██████╔╝\n{red}⢳⣿⣿⣿⠀ {bold}{Program.version}{red}⠀ ⢹⣿⡿⡁{orange}     ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚══════╝╚══════╝╚═════╝░\n{red}⠀⠹⣿⣿⡄⠀⠀⠀⠀⠀⢠⣿⡞⠁ {orange}         {bold}Admin: {f'{green}•{end}' if isAdmin() else f'{red}•{end}'}                                  {bold}@{underline}gental{end}\n{red}⠀⠀⠈⠛⢿⣄⠀⠀⠀⣠⠞⠋⠀⠀ {orange}                                                        \n{red}⠀⠀⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⠀⠀⠀{end}""")

def DrawMenu_Help():
    DrawBanner()
    print(f"""
{blue}COMMANDS.{end}
    {bold}:..{end}           Go to previous directory.
    {bold}:cd <dir>{end}     Go to <dir> directory.
    {bold}:sel <file>{end}   Select file.
    {bold}:dsel <dir>{end}   Select dir.
    {bold}:unsel{end}        Unselect file.
    {bold}:dunsel{end}       Unselect dir.
    {bold}:disk <disk>{end}  Change working disk.
    {bold}:movf{end}         Move selected file to selected directory.
    {bold}:copyf{end}        Copy selected file to selected directory.
    {bold}:refr{end}         Refresh filetree.
    {bold}:copyd{end}        Copy selected dir to {underline}current location{end}.
    {bold}:movd{end}         Move selected dir to {underline}current location{end}
    {bold}:help{end}         Display this help message.
    {bold}:find{end}         Open find file menu.
    {bold}:cleardisk{end}    Open cleardisk menu
    {bold}:open{end}         Open and write selected file content.

{blue}SYSTEM COMMANDS{end}
    {bold}::checkexist{end}         Check if logs and config files exists.
    {bold}::logs [show/clear]{end}  Read or clear logs file.
    {bold}::ver{end}                Display program version.
    {bold}::checkexist{end}         Check and repair basic problems with files.
    {bold}::cfg [show]{end}         Show current configuration.
    {bold}::cfg [refresh]{end}      Refresh configuration.
    {bold}::cfg [check]{end}        Check configuration and repair more advanced problems.
    {bold}::cfg [set] <entryName> <newValue>{end}  Change configuration setting. Use \"0\"-Off or \"1\"-On to set value.
    {bold}::update [check]{end}     Check for updates.
    {bold}::update [make]{end}      Install update. 

{blue}CONFIGURATION{end}
    {bold}Configuration also contains saved files locations!{end}
    {bold}Configuration file location:{end} {underline}C:\\Users\\{gp.getuser()}\\AppData\\Local\\.fira\\config.ini{end}
    {bold}Available settings:{end} <show_banner>, <auto_completion>, <auto_update>, <save_selected_file>, <save_selected_dir>, <save_current_path>

    """)
    WaitForEnter()

def DebugMode():
    #TODO: Make this func.
    pass


# Code update.
class Update:
    def CheckUpdate():
        url = "https://raw.githubusercontent.com/gental-py/fira/update/ver"
        Files.Logs.CreateLog("Info", "- CheckUpdate process started. -")

        try:
            currentVersion = Program.version
            newestVersion = float(r.get(url).text)
            Files.Logs.CreateLog("Info", f"| Online version: {newestVersion}")

            if newestVersion > currentVersion:
                Files.Logs.CreateLog("Info", f"- CheckUpdate process ended with: Update -")
                return True

            else:
                Files.Logs.CreateLog("Info", f"- CheckUpdate process ended with: No update -")
                return False

        except Exception as e:
            Files.Logs.CreateLog("Error", f"Cannot get newest version information from server. {e}")
            Files.Logs.CreateLog("Info", f"- CheckUpdate process ended with: Error -")
            return False

    def MakeUpdate():
        Files.Logs.CreateLog("Info", "- MakeUpdate process started. -") 

        # Get code.
        try:
            mainCodeURL = "https://raw.githubusercontent.com/gental-py/fira/update/updater.py"
            mainCodeREQ = r.get(mainCodeURL).text
            Files.Logs.CreateLog("Info", f"| Fetched code. (len={len(mainCodeREQ)})") 

        except Exception as e:
            Files.Logs.CreateLog("Error", f"| Cannot fetch code. {e}")
            Files.Logs.CreateLog("Info", "- MakeUpdate process ended with: Error. -")
            return False 

        # Create file.
        try:
            if os.path.exists("./updater.py"):
                Files.Logs.CreateLog("Warn", f"| updater.py actually exist.")
                try:
                    os.remove("./updater.py")
                    Files.Logs.CreateLog("Info", f"| | updater.py deleted.")

                except Exception as e:
                    Files.Logs.CreateLog("Error", f"| | Cannot delete updater.py: {e}")
                    Files.Logs.CreateLog("Info", "- MakeUpdate process ended with: Error. -")
                    return False

            open("./updater.py", "a+").close()
            Files.Logs.CreateLog("Info", f"| updater.py created.")

        except Exception as e:
            Files.Logs.CreateLog("Error", f"| Cannot create updater.py: {e}")
            Files.Logs.CreateLog("Info", "- MakeUpdate process ended with: Error. -")
            return False

        # Write to file.
        try:
            with open("./updater.py", "w", encoding="utf-8", newline="") as file:
                file.write(mainCodeREQ)

        except Exception as e:
            Files.Logs.CreateLog("Error", f"| Cannot write to updater.py: {e}")
            Files.Logs.CreateLog("Info", "- MakeUpdate process ended with: Error. -")    
            return False

        # Continue process in updater.py
        Files.Logs.CreateLog("Info", "| Files prepared. Continuing in module.")   
        Files.Logs.CreateLog("Info", "- MakeUpdate process ended with: OK. -")   
        os.system("py updater.py || python updater.py || python3 updater.py")


# Input validators.
class PathInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if not os.path.exists(text) and text != "" and text != ":back":
            raise ValidationError(message="This path does not exists!")

class TargetInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if text.replace(" ","") == "":
            raise ValidationError(message="Target cannot be blank!")

class DiskConfirmationInputValidator(Validator):
    def validate(self, document):
        text = document.text

        if text.replace(" ","") == "":
            raise ValidationError(message="Input cannot be blank!")

        if text not in ("x", "no", "n", "0", "v", "yes", "y", "1", ":back"):
            raise ValidationError(message="Invalid input.")

class ManualInputValidator(Validator):
    FILE_SELECTED_NAME = ""
    FILE_SELECTED = False
    DIR_SELECTED_NAME = ""
    DIR_SELECTED = False
    ALL_DISKS = []
    PREFIXES = []
    FILES = []
    DIRS = []

    def validate(self, document):
        text = document.text
        parsed_text = argParse(text)

        if text.replace(" ","") == "":
            raise ValidationError(message="Input cannot be blank!")

        if not text.startswith(ManualInputValidator.PREFIXES):
            raise ValidationError(message="None command prefix!")

        if text.startswith(":disk"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No disk specifed!")

            if parsed_text[1]+"\\" not in ManualInputValidator.ALL_DISKS:
                raise ValidationError(message="Invalid disk!")
      
        if text.startswith(":cd"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No directory specifed!")

            if parsed_text[1] not in ManualInputValidator.DIRS:
                raise ValidationError(message="Invalid directory!")

        if text.startswith(":sel"):
            if len(parsed_text) < 2:
                raise ValidationError(message=f"No file specifed!")

            if parsed_text[1] not in ManualInputValidator.FILES:
                raise ValidationError(message="Invalid file!")

        if text.startswith(":dsel"):
            if len(parsed_text) < 2:
                raise ValidationError(message=f"No dir specifed!")

            if parsed_text[1] not in ManualInputValidator.DIRS:
                raise ValidationError(message="Invalid dirname!")

        if text.startswith(":unsel"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

        if text.startswith(":dunsel"):
            if not ManualInputValidator.DIR_SELECTED:
                raise ValidationError(message="No dir selected!")

        if text.startswith(":movf"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

            if not ManualInputValidator.DIR_SELECTED:
                raise ValidationError(message="No directory selected!")

        if text.startswith(":copyf"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

            if os.path.abspath(ManualInputValidator.FILE_SELECTED_NAME) in ManualInputValidator.FILES:
                raise ValidationError(message="File with this name actually exists in this location!")

            if not ManualInputValidator.DIR_SELECTED:
                raise ValidationError(message="No directory selected!")

        if text.startswith(":copyd"):
            if not ManualInputValidator.DIR_SELECTED:
                raise ValidationError(message="No file selected!")

            if f"[{ManualInputValidator.DIR_SELECTED_NAME}]" in ManualInputValidator.DIRS:
                raise ValidationError(message="Dir with this name actually exists in this location!")

        if text.startswith(":open"):
            if not ManualInputValidator.FILE_SELECTED:
                raise ValidationError(message="No file selected!")

        if text.startswith("::logs"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No clear/show action.")

            if parsed_text[1].lower() not in ["clear", "show"]:
                raise ValidationError(message="Invalid parameter!")
        
        if text.startswith("::cfg"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No show/check/refresh/set action.")

            if parsed_text[1].lower() not in ["show", "check", "refresh", "set"]:
                raise ValidationError(message="Invalid parameter!")

            if parsed_text[1].lower() == "set":
                if len(parsed_text) != 4:
                    raise ValidationError(message=f"Invalid parameters amount! {len(parsed_text)}/4")

                if parsed_text[2] not in ["show_banner", "auto_update", "auto_completion", "save_selected_file", "save_selected_dir", "save_current_path"]:
                    raise ValidationError(message=f"Invalid <entryName> parameter!")

                if parsed_text[3] not in ["0", "1"]:
                    raise ValidationError(message="Invalid <newValue> parameter! (Possible: \"0\" - Off  /  \"1\" - On)")
                    
        if text.startswith("::update"):
            if len(parsed_text) < 2:
                raise ValidationError(message="No check/make action.")

            if parsed_text[1].lower() not in ["check", "make"]:
                raise ValidationError(message="Invalid parameter!")


# Config.
class Configuration:
    showBanner = True
    autoUpdate = True
    autoCompletion = True
    saveSelectedDir = True
    saveCurrentPath = True
    saveSelectedFile = True


# Files.
class Files:
    configCP = cp.ConfigParser()

    mainFolderLOC = f"C:\\Users\\{gp.getuser()}\\AppData\\Local\\.fira\\"
    configLOC = mainFolderLOC + "config.ini"
    logsLOC = mainFolderLOC + "logs.log"

    def CheckExistance():
        logs, config, main = Files.logsLOC, Files.configLOC, Files.mainFolderLOC
        anyError = False

        # Main folder.
        if not os.path.exists(os.path.abspath(main)):
            try:
                os.mkdir(main)

            except Exception as e:
                print(f"              {gray}[ {red}Error: {bold}Cannot create main folder. {e}{gray}]{end}")
                anyError = True
            
        # Logs file.
        if not os.path.exists(os.path.abspath(logs)):
            try:
                open(logs, "a+").close()

            except Exception as e:
                print(f"              {gray}[ {red}Error: {bold}Cannot create logs file. {e}{gray}]{end}")
                anyError = True

        # Config file.
        if not os.path.exists(os.path.abspath(config)):
            try:
                open(config, "a+").close()

            except Exception as e:
                print(f"              {gray}[ {red}Error: {bold}Cannot create config file. {e}{gray}]{end}")
                anyError = True

        if anyError: 
            WaitForEnter()

        return anyError

    def CheckConfigFile():
        Files.Logs.CreateLog("Info", f"- CheckConfigFile process started. -")
        Files.configCP.read(Files.configLOC)
        anyProblem = False

        # Check sections.
        sections = Files.configCP.sections()

        if "cfg" not in sections:
            Files.Logs.CreateLog("Warn", f"| CONFIG: Missing section: [cfg]")
            Files.configCP["cfg"] = {}
            anyProblem = True

        if "save" not in sections:
            Files.Logs.CreateLog("Warn", f"| CONFIG: Missing section: [save]")
            Files.configCP["save"] = {}
            anyProblem = True

        with open(Files.configLOC, "w") as f:
            Files.configCP.write(f)


        # Check entries in [cfg].
        entires = Files.configCP.items("cfg")
        allEntries = ["show_banner", "auto_update","auto_completion", "save_selected_file", "save_selected_dir", "save_current_path"]

        for entry in entires:
            if entry[0] in allEntries:
                allEntries.remove(entry[0])
                if entry[1] in ("1", "0"):
                    continue

                else:
                    Files.Logs.CreateLog("Warn", f"| CONFIG: Invalid value at: <{entry[0]}> = <{entry[1]}>")
                    Files.configCP["cfg"][entry[0]] = "1"
                    anyProblem = True
                
        if allEntries != []:
            for entry in allEntries:
                Files.Logs.CreateLog("Warn", f"| CONFIG: Missing entry: <{entry}>")
                Files.configCP["cfg"][entry] = "1"
                anyProblem = True

        with open(Files.configLOC, "w") as f:
            Files.configCP.write(f)

        # Check entries in [save]
        entries = Files.configCP.items("save")
        allEntriesSave = ["file", "dir", "current"]

        for entry in entries:
            if entry[0] in allEntriesSave:
                allEntriesSave.remove(entry[0])
                if os.path.exists(os.path.abspath(entry[1])):
                    continue

                else:
                    Files.Logs.CreateLog("Warn", f"| SAVE: Invalid path value at: <{entry[0]}> = <{entry[1]}>")
                    Files.configCP["save"][entry[0]] = ""
                    anyProblem = True

            else:
                Files.Logs.CreateLog("Warn", f"| SAVE: Unknown entry: <{entry[0]}>")
                Files.configCP.remove_option("save", entry[0])
                anyProblem = True
                
        if allEntriesSave != []:
            for entry in allEntriesSave:
                Files.Logs.CreateLog("Warn", f"| SAVE: Missing entry: <{entry}>")
                Files.configCP["save"][entry] = ""
                anyProblem = True

        # Check if values are not set when they are disabled in config.
        if Configuration.saveSelectedFile == False:
            Files.configCP["save"]["file"] = ""
        if Configuration.saveSelectedDir == False:
            Files.configCP["save"]["dir"] = ""
        if Configuration.saveCurrentPath == False:
            Files.configCP["save"]["current"] = ""
            

        with open(Files.configLOC, "w") as f:
            Files.configCP.write(f)

        
        Files.Logs.CreateLog("Info", f"- CheckConfigFile process ended with: {anyProblem} -")
        return anyProblem

    def LoadSavedPaths(): 
        Files.configCP.read(Files.configLOC)
        if Configuration.saveSelectedFile:
            try: 
                filePath = os.path.abspath(Files.configCP["save"]["file"])
                if not os.path.exists(filePath):
                    Files.Logs.CreateLog("Error", f"Saved file path does not exists.")
                    filePath = None
                else:
                    Manual.Important.selected_fileLOC = filePath
                    Manual.Important.selected_fileNAME = os.path.basename(filePath)

            except Exception as e:
                Files.Logs.CreateLog("Error", f"Cannot load saved file. {e}")
                filePath = None

        if Configuration.saveSelectedDir:
            try: 
                dirPath = os.path.abspath(Files.configCP["save"]["dir"])+"\\"
                if not os.path.exists(dirPath):
                    Files.Logs.CreateLog("Error", f"Saved dir path does not exists.")
                    dirPath = None
                else:
                    Manual.Important.selected_dirLOC = dirPath
                    Manual.Important.selected_dirNAME = dirPath.split("\\")[-2]+"\\"

            except Exception as e:
                Files.Logs.CreateLog("Error", f"Cannot load saved dir. {e}")
                dirPath = None

        if Configuration.saveCurrentPath:
            try: 
                currentPath = os.path.abspath(Files.configCP["save"]["current"])
                if not os.path.exists(currentPath):
                    Files.Logs.CreateLog("Error", f"Saved current path does not exists.")
                    currentPath = None
                else:
                    Manual.Important.current = currentPath

            except Exception as e:
                Files.Logs.CreateLog("Error", f"Cannot load saved current path. {e}")
                currentPath = None   

    
    class Logs:
        def CreateLog(type, content):
            date, time = datetime.today().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M")
            log = f"[ {date}  -  {time} ]  [ {type} ]  ~  {content}\n"
            if type == "Startup": log = "\n"+log
            if type == "Error": log = f"[ {date}  -  {time} ]  [ {type} ] ~  {content}\n"

            with open(Files.logsLOC, "a") as file:
                file.write(log)

        def ClearLogs():
            open(Files.logsLOC, "w+").close()
            Files.Logs.CreateLog("Info", f"--- Logs cleared by command. ---")


    class Config:
        def ReadConfig():
            Files.configCP.read(Files.configLOC)
            Files.Logs.CreateLog("Info", f"- ReadConfig process started. -")

            try:
                Configuration.showBanner = Files.configCP["cfg"]["show_banner"]
                if Configuration.showBanner == "1": Configuration.showBanner = True
                else: Configuration.showBanner = False
                Files.Logs.CreateLog("Info", f"| | <show_banner> : {Configuration.showBanner}")

                Configuration.autoCompletion = Files.configCP["cfg"]["auto_completion"]
                if Configuration.autoCompletion == "1": Configuration.autoCompletion = True
                else: Configuration.autoCompletion = False
                Files.Logs.CreateLog("Info", f"| | <auto_completion> : {Configuration.autoCompletion}")

                Configuration.autoUpdate = Files.configCP["cfg"]["auto_update"]
                if Configuration.autoUpdate == "1": Configuration.autoUpdate = True
                else: Configuration.autoUpdate = False

                Configuration.saveSelectedFile = Files.configCP["cfg"]["save_selected_file"]
                if Configuration.saveSelectedFile == "1": Configuration.saveSelectedFile = True
                else: Configuration.saveSelectedFile = False
                Files.Logs.CreateLog("Info", f"| | <save_selected_file> : {Configuration.saveSelectedFile}")

                Configuration.saveSelectedDir = Files.configCP["cfg"]["save_selected_dir"]
                if Configuration.saveSelectedDir == "1": Configuration.saveSelectedDir = True
                else: Configuration.saveSelectedDir = False
                Files.Logs.CreateLog("Info", f"| | <save_selected_dir> : {Configuration.saveSelectedDir}")

                Configuration.saveCurrentPath = Files.configCP["cfg"]["save_current_path"]
                if Configuration.saveCurrentPath == "1": Configuration.saveCurrentPath = True
                else: Configuration.saveCurrentPath = False
                Files.Logs.CreateLog("Info", f"| | <save_current_path> : {Configuration.saveCurrentPath}")

                Files.Logs.CreateLog("Info", f"| Succesfully readed and set configs.")
                Files.Logs.CreateLog("Info", f"- ReadConfig process ended with: False. -")
                return False

            except Exception as e:
                Files.Logs.CreateLog("Error", f"| Cannot read configuration file. {e}")
                Files.Logs.CreateLog("Info", f"- ReadConfig process ended with: True. -")
                return True

        def ChangeConfig(entryName, newContent):
            try:
                Files.configCP.read(Files.configLOC)
                entryValue_Before = Files.configCP["cfg"][entryName]
                Files.configCP["cfg"][entryName] = newContent
                with open(Files.configLOC, "w") as f:
                    Files.configCP.write(f)

                Files.Logs.CreateLog("Info", f"CONFIG: Changed <{entryName}> value.  {entryValue_Before} -> {newContent}")
                Files.CheckConfigFile()
                Files.Config.ReadConfig()

            except Exception as e:
                Files.Logs.CreateLog("Error", f"CONFIG: Cannot change <{entryName}> value. {e}")

        def ChangeSavedPath(type, path):
            if type == "file":
                Files.configCP["save"]["file"] = path

            if type == "dir":
                Files.configCP["save"]["dir"] = path 

            if type == "current":
                Files.configCP["save"]["current"] = path

            with open(Files.configLOC, "w") as f:
                Files.configCP.write(f)


# Check for update.
if Update.CheckUpdate():
    print(f"{bold}New version available!{end}")
    if Configuration.autoUpdate:
        Update.MakeUpdate()

    else:
        print(f"{bold}To install new version, type:{end}  ::update make")
        WaitForEnter()


# Operations section.
class Manual:
    
    class Important:
        # :..                Go to previous directory.
        # :cd <folder>       Go to folder.
        # :sel <file>        Select file to operate on. 
        # :dsel <dir>        Select dir to operate on.
        # :unsel             Clear selection.
        # :dunsel            Clear dir selection.
        # :disk <disk>       Set work disk.
        # :movf              Move selected file to selected dir location.
        # :copyf             Copy and paste selected file to selected dir location.
        # :refr              Refresh filetree.
        # :copyd             Copy and paste selected directory to current location.
        # :movd              Move selected dir to current location.
        # :help              Print help page.
        # :find              Find file. 
        # :cleardisk         Clear disk from temp files.
        # :open              Open selected file.
        # ::checkexist       Check if settings and logs file exists.
        # ::cfg [check]      Check config file health.
        # ::cfg [refresh]    Refresh config.
        # ::cfg [show]       Display current configuration.    
        # ::cfg [set]     Change config.
        # ::logs [clear]     Clear logs file.
        # ::logs [show]      Write logs file content.
        # ::ver              Display program version.
        # ::update [check]   Check for updates.
        # ::update [make]    Make update if there's newer version. 

        current = os.getcwd()
        selected_fileLOC = None
        selected_fileNAME = None
        selected_dirNAME = None
        selected_dirLOC = None
        prompt_session = PromptSession()
        allDisks = re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
        actions = ("::update","::dev","::cfg", "::ver", "::logs", "::checkexist", ":open", ":cleardisk", ":find", ":help", ":exit", ":refr", ":cd", ":sel", ":unsel", ":..", ":disk", ":movf", ":copyf", ":dsel", ":dunsel", ":copyd", ":movd")
        ManualInputValidator.PREFIXES = actions
        ManualInputValidator.ALL_DISKS = allDisks
    

    def Main():
        # Main loop
        while True:
            DrawBanner()
            
            # Fetch files and folders.
            wc_Dirs = []
            wc_Files = []

            for obj in os.listdir(Manual.Important.current):
                if not os.path.isdir(f"{Manual.Important.current}\\{obj}"): wc_Files.append(obj)
                else: wc_Dirs.append(f"[{obj}]")

            ManualInputValidator.DIRS = wc_Dirs
            ManualInputValidator.FILES = wc_Files


            # Draw file tree
            print(f"\n\n  {cyan}╭─< {bold}{Manual.Important.current} {cyan}>•{end}\n  {cyan}│{end}")
            for dir in wc_Dirs: 
                if dir.replace("[", "", 1)[:-1]+"\\" == Manual.Important.selected_dirNAME and os.path.abspath(Manual.Important.current+"\\"+Manual.Important.selected_dirNAME+"\\") == os.path.abspath(Manual.Important.selected_dirLOC+"\\"): print(f"{purple}->{cyan}├ {blink}{bold}{dir}{end}")
                else: print(f"  {cyan}├ {bold}{dir}{end}")

            print(f"  {blue}⋮{end}")
            for file in wc_Files:
                if file == Manual.Important.selected_fileNAME and os.path.abspath(Manual.Important.current+"\\"+Manual.Important.selected_fileNAME) == os.path.abspath(Manual.Important.selected_fileLOC): print(f"{orange}->{cyan}├ {blink}{bold}{file}{end}")
                else: print(f"  {cyan}├ {bold}{file}{end}")

            print(f"  {cyan}╰{red}•{end}")


            # Auto completer.
            Completer = NestedCompleter.from_nested_dict({
                ':help': None, 
                ':cd': WordCompleter(wc_Dirs),
                ':..': None, 
                ':sel': WordCompleter(wc_Files),
                ':dsel': WordCompleter(wc_Dirs),
                ':unsel': None,
                ':dunsel': None,
                ':disk': WordCompleter(Manual.Important.allDisks),
                ':movf': None,
                ':copyf': None,
                ':movd': None,
                ':copyd': None,
                ':open': None,
                ':find': None,
                ':cleardisk': None,
                ':refr': None,
                ':exit': None,
                '::checkexist': None,
                '::logs': WordCompleter(['clear', 'show']),
                '::ver': None,
                '::checkcfg': None,
                '::update': WordCompleter(['check', 'make']),
                '::cfg': {
                    'show': None, 
                    'check': None, 
                    'refresh': None,
                    'set': {
                        'show_banner': WordCompleter(['0', '1']),
                        'auto_completion': WordCompleter(['0', '1']),
                        'auto_update': WordCompleter(['0', '1']),
                        'save_selected_file': WordCompleter(['0', '1']),
                        'save_selected_dir': WordCompleter(['0', '1']),
                        'save_current_path': WordCompleter(['0', '1']),
                    }
                }
            })


            if not Configuration.autoCompletion: Completer = NestedCompleter.from_nested_dict({})
            

            # Bottom toolbar.
            def BottomToolbar(current, selectedfile, selecteddir):
                return HTML(f'Current path:  <b><style bg="ansiblue">{current} </style></b>\nSelected file: <b><style bg="ansiyellow">{selectedfile} </style></b>\nSelected dir:  <b><style bg="ansipurple">{selecteddir} </style></b>')


            # Get action
            action = Manual.Important.prompt_session.prompt(f'\n  ~ ', completer=Completer, validator=ManualInputValidator(), bottom_toolbar=BottomToolbar(Manual.Important.current, Manual.Important.selected_fileLOC, Manual.Important.selected_dirLOC), auto_suggest=AutoSuggestFromHistory())
            parsed_action = argParse(action)

            if parsed_action[0] == "::dev":
                pass

            if parsed_action[0] == ":exit": exit()

            if parsed_action[0] == ":refr": continue

            if parsed_action[0] == ":help": DrawMenu_Help()

            if parsed_action[0] == ":..":
                Manual.Important.current = os.path.dirname(Manual.Important.current)
                if Configuration.saveCurrentPath:
                    Files.Config.ChangeSavedPath("current", Manual.Important.current)
                
            if parsed_action[0] == ":disk":
                Manual.Important.current = parsed_action[1] + "\\"
                if Configuration.saveCurrentPath:
                    Files.Config.ChangeSavedPath("current", Manual.Important.current)

            if parsed_action[0] == ":cd":
                Manual.Important.current += "\\"+parsed_action[1].replace("[", "", 1)[:-1]
                if Configuration.saveCurrentPath:
                    Files.Config.ChangeSavedPath("current", Manual.Important.current)

            if parsed_action[0] == ":sel":
                Manual.Important.selected_fileLOC = os.path.abspath(Manual.Important.current+"\\"+parsed_action[1])
                Manual.Important.selected_fileNAME = parsed_action[1]
                ManualInputValidator.FILE_SELECTED = True
                ManualInputValidator.FILE_SELECTED_NAME = Manual.Important.selected_fileNAME

                if Configuration.saveSelectedFile:
                    Files.Config.ChangeSavedPath("file", Manual.Important.selected_fileLOC)

            if parsed_action[0] == ":unsel":
                Manual.Important.selected_fileLOC = None
                Manual.Important.selected_fileNAME = None
                ManualInputValidator.FILE_SELECTED = False
                ManualInputValidator.FILE_SELECTED_NAME = None

                if Configuration.saveSelectedFile:
                    Files.Config.ChangeSavedPath("file", "")

            if parsed_action[0] == ":dsel":
                Manual.Important.selected_dirLOC = os.path.abspath(Manual.Important.current+"\\"+parsed_action[1].replace("[", "", 1)[:-1]+"\\")
                Manual.Important.selected_dirNAME = parsed_action[1].replace("[", "", 1)[:-1]+"\\"
                ManualInputValidator.DIR_SELECTED = True
                ManualInputValidator.DIR_SELECTED_NAME = parsed_action[1].replace("[", "", 1)[:-1]+"\\"

                if Configuration.saveSelectedFile:
                    Files.Config.ChangeSavedPath("dir", Manual.Important.selected_dirLOC)

            if parsed_action[0] == ":dunsel":
                Manual.Important.selected_dirLOC = None
                Manual.Important.selected_dirNAME = None
                ManualInputValidator.DIR_SELECTED_NAME = None
                ManualInputValidator.DIR_SELECTED = False

                if Configuration.saveSelectedFile:
                    Files.Config.ChangeSavedPath("dir", "")
                
            if parsed_action[0] == ":movf":
                try:
                    shutil.move(Manual.Important.selected_fileLOC, os.path.abspath(Manual.Important.selected_dirLOC+"\\"+Manual.Important.selected_fileNAME))
                    Files.Logs.CreateLog("Info", f"MoveFile: {Manual.Important.selected_fileLOC} -> {os.path.abspath(Manual.Important.selected_dirLOC+'/'+Manual.Important.selected_fileNAME)}")
                    Manual.Important.selected_fileLOC = os.path.abspath(Manual.Important.selected_dirLOC+"\\"+Manual.Important.selected_fileNAME)

                    if Configuration.saveSelectedFile:
                        Files.Config.ChangeSavedPath("file", Manual.Important.selected_fileLOC)

                except Exception as e:
                    DrawBanner()
                    print(f"              {gray}[ {red}Error: {bold}Cannot move file. {e}{gray}]{end}")
                    Files.Logs.CreateLog("Error", f"MoveFile: {Manual.Important.selected_fileLOC} -> ERROR: {{{e}}}")
                    WaitForEnter()

            if parsed_action[0] == ":movd":
                try:
                    shutil.move(Manual.Important.selected_dirLOC, Manual.Important.current+"\\"+Manual.Important.selected_dirNAME)
                    Files.Logs.CreateLog("Info", f"MoveDir: {Manual.Important.selected_dirLOC} -> {os.path.abspath(Manual.Important.selected_dirLOC+'/'+Manual.Important.selected_dirNAME)}")

                    if Configuration.saveSelectedFile:
                        Files.Config.ChangeSavedPath("dir", Manual.Important.selected_dirLOC)

                except Exception as e:
                    DrawBanner()
                    print(f"              {gray}[ {red}Error: {bold}Cannot copy dirtree. {e}{gray}]{end}")
                    Files.Logs.CreateLog("Error", f"MoveDir: {Manual.Important.selected_dirLOC} -> ERROR: {{{e}}}")
                    WaitForEnter()

            if parsed_action[0] == ":copyf":
                try:
                    shutil.copyfile(Manual.Important.selected_fileLOC, os.path.abspath(Manual.Important.selected_dirLOC+"\\"+Manual.Important.selected_fileNAME))
                    Files.Logs.CreateLog("Info", f"CopyFile: {Manual.Important.selected_fileLOC} -> {os.path.abspath(Manual.Important.selected_dirLOC+'/'+Manual.Important.selected_fileNAME)}")

                except Exception as e:
                    DrawBanner()
                    print(f"              {gray}[ {red}Error: {bold}Cannot copy file. {e}{gray}]{end}")
                    Files.Logs.CreateLog("Error", f"CopyFile: {Manual.Important.selected_fileLOC} -> ERROR: {{{e}}}")
                    WaitForEnter()

            if parsed_action[0] == ":copyd":
                try:
                    shutil.copytree(Manual.Important.selected_dirLOC, Manual.Important.current+"\\"+Manual.Important.selected_dirNAME)
                    Files.Logs.CreateLog("Info", f"CopyDir: {Manual.Important.selected_dirLOC} -> {os.path.abspath(Manual.Important.selected_dirLOC+'/'+Manual.Important.selected_dirNAME)}")

                except Exception as e:
                    DrawBanner()
                    print(f"              {gray}[ {red}Error: {bold}Cannot copy dirtree. {e}{gray}]{end}")
                    Files.Logs.CreateLog("Error", f"CopyDir: {Manual.Important.selected_dirLOC} -> ERROR: {{{e}}}")
                    WaitForEnter()

            if parsed_action[0] == ":find":
                Automatic.FindFile()

            if parsed_action[0] == ":cleardisk":
                Automatic.CleanDisks()

            if parsed_action[0] == ":open":
                Automatic.OpenFile()

            if parsed_action[0] == "::checkexist":
                checkexist_status = Files.CheckExistance()
                print(f"{bold}Status: {red if checkexist_status else green}{checkexist_status}{end}")
                WaitForEnter()
                
            if parsed_action[0] == "::logs":
                if parsed_action[1] == "clear":
                    Files.Logs.ClearLogs()
                    print(f"{bold}Cleared logs file.{end}")
                if parsed_action[1] == "show":
                    with open(Files.logsLOC, 'r') as file:
                        print(*file.readlines())
                WaitForEnter()

            if parsed_action[0] == "::ver":
                print(f"{bold}Version: {Program.version}{end}")
                WaitForEnter()

            if parsed_action[0] == "::cfg":
                if parsed_action[1] == "show":
                    print(f"{blue}Current config:{end}\n  {bold}showBanner{end} : {green if Configuration.showBanner else red}{Configuration.showBanner}\n  {bold}autoCompletion{end} : {green if Configuration.autoCompletion else red}{Configuration.autoCompletion}\n  {bold}saveSelectedFile{end} : {green if Configuration.saveSelectedFile else red}{Configuration.saveSelectedFile}\n  {bold}saveSelectedDir{end} : {green if Configuration.saveSelectedDir else red}{Configuration.saveSelectedDir}\n  {bold}saveCurrentPath{end} : {green if Configuration.saveCurrentPath else red}{Configuration.saveCurrentPath}")
                    WaitForEnter()

                if parsed_action[1] == "check":
                    checkcfg_status = Files.CheckConfigFile()
                    print(f"{bold}Status: {red if checkcfg_status else green}{'Some problems detected. Check logs for more info.' if checkcfg_status else 'None problems found.'}{end}")
                    WaitForEnter()

                if parsed_action[1] == "refresh":
                    refreshcfg_status = Files.Config.ReadConfig()
                    print(f"{bold}Status: {red if refreshcfg_status else green}{'Some problems detected. Check logs for more info.' if refreshcfg_status else 'None problems found.'}{end}")
                    WaitForEnter()

                if parsed_action[1] == "set":
                    Files.Config.ChangeConfig(parsed_action[2], parsed_action[3])

            if parsed_action[0] == "::update":
                if parsed_action[1] == "check":
                    updatecheck_status = Update.CheckUpdate()
                    print(f"{bold}Status: {red if not updatecheck_status else green}{'No update detected.' if not updatecheck_status else 'Update available!'}")
                    WaitForEnter()

                if parsed_action[1] == "make":
                    if Update.CheckUpdate():
                        if not Update.MakeUpdate():
                            print(f"{red}Cannot make update. Check logs for more info.{end}")
                            WaitForEnter()
                    else:
                        print(f"{red}No newer version available.{end}")
                        WaitForEnter()


class Automatic:

    def FindFile():
        DrawBanner()

        def toolbar_BackHint():
            return HTML(f'<b><style bg="ansired">:back</style> <style bg="ansiblue">- Cancel operation.</style></b>')

        # Fetch data.
        target, location, allHits, allDisks = "", "", [], re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
             
        target = prompt('                         Target ~ ', validator=TargetInputValidator(), bottom_toolbar=toolbar_BackHint)
        if target.replace(" ", "").lower() == ":back": return
        location = prompt('                       Location ~ ', validator=PathInputValidator(), bottom_toolbar=toolbar_BackHint)
        if location == ":back": return

        # Find file(s).
        print(f"                          {bold}Searching . . .{end}")

        if location != "": allDisks = [location]
        for disk in allDisks:
            for root, dirs, files in os.walk(disk):
                for file in files:
                    if fnmatch.fnmatch(file, target):
                        allHits.append(os.path.join(root, file))
        

        # Print results.
        DrawBanner()
        print(f"                          {red}• {bold}Found {orange}{len(allHits)} {bold}file(s).{end}\n")
        for hit in allHits: print(f"                 {orange}• {bold}{hit}{end}")
        WaitForEnter()

    def CleanDisks():
        allDisks = []
        disksStatus = []
        for disk in re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE):
            allDisks.append({"name": disk, "state": False})

        # Select disk(s)
        def DisplaySelection():
            DrawBanner()

            print(f"                      {bold}Select which disks you want to be cleaned.{end}\n\n")
            for disk in allDisks:
                print(f"                           {orange}• {bold}{disk['name']} {gray}: {f'{green}v{end}' if disk['state'] else f'{red}x{end}'}")

        def BottomToolbar():
            return HTML('<b><style bg="ansigreen">v, yes, y, 1</style></b> <style bg="gray">//</style> <b><style bg="red">x, no, n, 0</style></b>   |   <b><style bg="ansired">:back</style> <style bg="ansiblue">- Cancel operation.</style></b>')

        for disk in allDisks:        
            DisplaySelection()

            state_input = prompt(f'\n                             {disk["name"]} ~ ', validator=DiskConfirmationInputValidator(), bottom_toolbar=BottomToolbar())
            if state_input == ":back": return
            if state_input in ("v", "yes", "y", "1"):
                disk["state"] = True
                disksStatus.append({"name": disk["name"], "TempFilesStatus": {"error": 0, "succes": 0, "total": 0}, "TempFoldersStatus": {"error": 0, "succes": 0, "total": 0}, "TempDirsStatus": {"error": 0, "succes": 0, "total": 0}})


        # Delete.
        DrawBanner()
        if not isAdmin():
            print(f"\n          {gray}[ {orange}Warn: {bold}Program is running without administrator permissions. May delete less files.{gray}]{end}")
        print(f"                                       {gray}[ {green}Info: {bold}Deleting process started.{gray}]{end}")

        for i, disk in enumerate(allDisks):
            if disk["state"] == False:
                continue

            # Delete .tmp files.
            for root, dirs, files in os.walk(disk["name"]):
                for file in files:
                    if file.endswith(".tmp"):
                        tmp_file_path = os.path.join(root, file)
                        disksStatus[i]["TempFilesStatus"]["total"] += 1

                        try:
                            os.remove(tmp_file_path)
                            disksStatus[i]["TempFilesStatus"]["succes"] += 1
                            
                        except:
                            disksStatus[i]["TempFilesStatus"]["error"] += 1

            # Delete files in Temp folder.
            if "c" in disk["name"].lower():
                temp_folder_path = f"C:\\Users\\{gp.getuser()}\\AppData\\Local\\Temp\\"

                try:
                    for root, dirs, files in os.walk(temp_folder_path):
                        for file in files:
                            folder_file_path = os.path.join(root, file)
                            disksStatus[i]["TempFoldersStatus"]["total"] += 1

                            try:
                                os.remove(folder_file_path)
                                disksStatus[i]["TempFoldersStatus"]["succes"] += 1

                            except:
                                disksStatus[i]["TempFoldersStatus"]["error"] += 1

                except Exception as TempFoldersStatusERROR:
                    disksStatus[i]["TempFoldersStatus"]["error"] = -1


                # Delete dirs in Temp folder
                try:
                    dirs = [f for f in os.listdir(temp_folder_path) if not os.path.isfile(os.path.join(temp_folder_path, f))]
                    for dir in dirs:
                        disksStatus[i]["TempDirsStatus"]["total"] += 1

                        try:
                            os.rmdir(temp_folder_path+dir)
                            disksStatus[i]["TempDirsStatus"]["succes"] += 1

                        except:
                            disksStatus[i]["TempDirsStatus"]["error"] += 1

                except Exception as TempDirsStatusERROR:
                    disksStatus[i]["TempDirsStatus"]["error"] = -1
                

        # Print results.
        DrawBanner()
        for disk in disksStatus:
            print(f"\n\n                {orange}• {bold}{disk['name']}{end}")
            print(f"                        {orange}╰• {bold}.tmp files:{end}")
            print(f"                            {blue}╰• Total: {disk['TempFilesStatus']['total']}{end}")
            print(f"                            {green}╰• Succes: {disk['TempFilesStatus']['succes']}{end}")
            print(f"                            {red}╰• Errors: {disk['TempFilesStatus']['error']}{end}")


            if "c" in disk["name"].lower():
                print(f"\n                        {orange}╰• {bold}Files in /Temp folder:{end}")
                print(f"                            {blue}╰• Total: {disk['TempFoldersStatus']['total']}{end}")
                print(f"                            {green}╰• Succes: {disk['TempFoldersStatus']['succes']}{end}")
                print(f"                            {red}╰• Errors: {f'Fatal error: {TempFoldersStatusERROR}' if disk['TempFoldersStatus']['error'] == -1 else disk['TempFilesStatus']['error']}{end}")

                print(f"\n                        {orange}╰• {bold}Dirs in /Temp folder:{end}")
                print(f"                            {blue}╰• Total: {disk['TempDirsStatus']['total']}{end}")
                print(f"                            {green}╰• Succes: {disk['TempDirsStatus']['succes']}{end}")
                print(f"                            {red}╰• Errors: {f'Fatal error: {TempDirsStatusERROR}' if disk['TempDirsStatus']['error'] == -1 else disk['TempDirsStatus']['error']}{end}")

        WaitForEnter()

    def OpenFile():
        FILE = Manual.Important.selected_fileLOC
        cls()
        try:
            FileOpen = open(FILE, "r", encoding="utf-8")
            _lines = FileOpen.readlines()

        except Exception as e:
            print(f"          {gray}[ {red}ERROR: {bold} An error ocured: {e}{gray}]{end}")
            WaitForEnter()
            return

        BlankLen = len(str(len(_lines)))
        for index, line in enumerate(_lines):
            line = line.replace('=',f'{blue}={end}').replace('(',f'{purple}({end}').replace(')',f'{purple}){end}').replace('"', f'{green}"{end}')
            for c in ["+", "-", "*", "/", "%", ":", "?", "|"]:
                line = line.replace(c, f'{orange}{c}{end}')

            print(f"{cyan}{' ' * int(BlankLen-len(str(index+1)))}{index+1} {gray}| {bold}{line}{end}",end="")

        FileOpen.close()
        WaitForEnter()


# Main.
while True:
    try:
        Files.CheckExistance()
        Files.Logs.CreateLog("Startup", f"--- New session. (v{Program.version})---")
        Files.CheckConfigFile()
        Files.LoadSavedPaths()
        Files.Config.ReadConfig()
        Manual.Main()

    except Exception as e:
        DrawBanner()
        print(f"{red}FATAL ERROR: {bold}{e}{end}")
        exit()


