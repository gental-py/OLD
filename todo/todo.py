import configparser as cp
import keyboard as k
import time as t
import os


# Clear screen
cls = lambda: os.system("cls || clear")
cls()


# Colors
orange = "\033[0;33m"
purple = "\033[1;35m"
green = "\033[1;32m"
white = "\033[1;37m"
cyan = "\033[1;36m"
gray = "\033[1;30m"
blue = "\033[1;34m"
red = "\033[1;31m"
end = "\033[0m"


# Program control main variables.
CursorShadow = 0
_Refresh = False
_Exit = False
_Cursor = 0


# Handle saved session.
SavedSessionFileLoc = ".\\session.ini"
SavedSessionCP = cp.ConfigParser()

if not os.path.exists(SavedSessionFileLoc):
    open(SavedSessionFileLoc, "a+").close()
    SavedSessionCP["session"] = {}
    with open(SavedSessionFileLoc, "w+") as saving:
        SavedSessionCP.write(saving)

SavedSessionCP.read(SavedSessionCP)


# Read settings.
SettingsFileLoc = ".\\settings.ini"
config = cp.ConfigParser()

if not os.path.exists(SettingsFileLoc):
    open(SettingsFileLoc, "a+").close() 
    config["settings"] = {"operation_key": "alt", "cursor_color_name": "purple", "wrap_cursor": "0", "names_contrast": "0", "cursor_char": ">"}
    with open(SettingsFileLoc, 'w+') as configuration:
        config.write(configuration)

config.read(SettingsFileLoc)


# Try to enter settings.
try:
    _OperationKey = config["settings"]["operation_key"]
    _CursorColorName = config["settings"]["cursor_color_name"]
    CursorColorVar = locals()[_CursorColorName]
    _WrapCursor = config["settings"]["wrap_cursor"]
    if int(_WrapCursor) == 1:
        _WrapCursor = True
    else:
        _WrapCursor = False
    _NamesContrast = config["settings"]["names_contrast"]
    if int(_NamesContrast) == 1:
        _NamesContrast = True
    else:
        _NamesContrast = False
    _CursorChar = config["settings"]["cursor_char"]
        
except Exception as e:
    print(f"{red}Settings error: {e}{end}")
    open(SettingsFileLoc, "a+").close() 
    config["settings"] = {"operation_key": "alt", "cursor_color_name": "purple", "wrap_cursor": "0", "names_contrast": "0", "cursor_char": ">"}
    with open(SettingsFileLoc, 'w+') as configuration:
        config.write(configuration)

    input(f"{gray}Press enter to restart app.{end}")
    os.system('py todo.py || python3 todo.py || python todo.py')
    exit()


# Main functions
def SaveSession():
    global _Tasks, SavedSessionCP, SavedSessionFileLoc

    # Clear file
    open(SavedSessionFileLoc, "w+").close()

    # Create "session"
    SavedSessionCP["session"] = {}
    with open(SavedSessionFileLoc, "w") as saving:
        SavedSessionCP.write(saving)

    # Put tasks into "session."
    for item in _Tasks:
        # Turn uppercase letter to ^a = A
        SaveName = ""
        for letter in item['name']:
            SaveName += letter if letter.islower() else f"%{letter.lower()}"
        
        SavedSessionCP["session"][SaveName] = str(item['state'])

    # Write changes to file.
    with open(SavedSessionFileLoc, "w") as saving:
        SavedSessionCP.write(saving)


def CursorControl():
    global _Cursor, _Exit, _Tasks, _WrapCursor, _Refresh

    if k.is_pressed((_OperationKey, "f1")):
        _Exit = True
        return
        
    elif k.is_pressed((_OperationKey, "f2")):
        os.system("py configurator.py || python3 configurator.py || python configurator.py")
        exit()

    # Save.
    elif k.is_pressed((_OperationKey, "f3")):
        SaveSession()

    # Delete task.
    elif k.is_pressed((_OperationKey, "f6")):
        if len(_Tasks) == 1:
            return

        try:
            print(f"{red}Delete: {end}{_Tasks[_Cursor]['name']}{red}?{end}")
        except:
            _Cursor = 0

        while True:
            try:
                TaskDeleteConfirmation = input(f"  {gray}[{green}Y{gray}/{red}n{gray}] >{end}").replace(" ","").lower()
            except EOFError:
                continue

            if TaskDeleteConfirmation == "y":
                _Tasks.pop(_Cursor)
                _Cursor = 0
                _Refresh = True
                break

            elif TaskDeleteConfirmation == "n":
                _Refresh = True
                break

            else:
                continue
        return

    # Add task.
    if k.is_pressed((_OperationKey, "f5")):
        ActuallyExistingTasks = []
        for task in _Tasks:
            ActuallyExistingTasks.append(task["name"])

        while True:
            NewTask = input(f"  {gray}New task name: {end}")
            if NewTask in ActuallyExistingTasks:
                print(f"  {red}This task actually exists!{end}")
                continue
            else:
                _Tasks.append({"state": 0, "name": NewTask})
                break

        _Refresh = True
        return

    if k.is_pressed((_OperationKey, "RIGHT")):
        _Tasks[_Cursor]["state"] += 1

        if _Tasks[_Cursor]["state"] == 4:
            _Tasks[_Cursor]["state"] = 0

        _Refresh = True
        t.sleep(0.3)
        return

    if k.is_pressed((_OperationKey, "LEFT")):
        _Tasks[_Cursor]["state"] -= 1

        if _Tasks[_Cursor]["state"] == -1:
            _Tasks[_Cursor]["state"] = 3

        _Refresh = True
        t.sleep(0.3)
        return

    elif k.is_pressed((_OperationKey, "UP")):
        if _WrapCursor:
            if _Cursor == 0:
                _Cursor = len(_Tasks) -1
            else:
                _Cursor -=1
        else:
            if _Cursor > 0:
                _Cursor -=1

        t.sleep(0.1)
        return
            
    elif k.is_pressed((_OperationKey, "DOWN")):
        if _WrapCursor:
            if _Cursor == len(_Tasks) -1:
                _Cursor = 0
            else:
                _Cursor += 1

        else:
            if _Cursor < len(_Tasks) -1:
                _Cursor += 1

        t.sleep(0.1)
        return

    else:
        return


def TaskControl():
    global _Cursor, _Tasks, _Refresh, _Exit
    while True:

        if k.is_pressed((_OperationKey, "UP")) or k.is_pressed((_OperationKey, "DOWN")):
            break

        # Exit.
        if k.is_pressed((_OperationKey, "f1")):
            _Exit = True
            break
        
        # Settings.
        if k.is_pressed((_OperationKey, "f2")):
            os.system("py configurator.py || python3 configurator.py || python configurator.py")
            exit()

        # Save.
        if k.is_pressed((_OperationKey, "f3")):
            SaveSession()

        # Delete task.
        if k.is_pressed((_OperationKey, "f6")):
            if len(_Tasks) == 1:
                break

            try:
                print(f"{red}Delete: {end}{_Tasks[_Cursor]['name']}{red}?{end}")
            except:
                _Cursor = 0
            while True:
                try:
                    TaskDeleteConfirmation = input(f"  {gray}[{green}Y{gray}/{red}n{gray}] >{end}").replace(" ","").lower()
                except EOFError:
                    continue

                if TaskDeleteConfirmation == "y":
                    _Tasks.pop(_Cursor)
                    _Cursor = 0
                    _Refresh = True
                    break

                elif TaskDeleteConfirmation == "n":
                    _Refresh = True
                    break

                else:
                    continue
            break

        # Add task.
        if k.is_pressed((_OperationKey, "f5")):
            ActuallyExistingTasks = []
            for task in _Tasks:
                ActuallyExistingTasks.append(task["name"])

            while True:
                NewTask = input(f"  {gray}New task name: {end}")
                if NewTask in ActuallyExistingTasks:
                    print(f"  {red}This task actually exists!{end}")
                    continue
                else:
                    _Tasks.append({"state": 0, "name": NewTask})
                    break

            _Refresh = True
            break

        if k.is_pressed((_OperationKey, "RIGHT")):
            _Tasks[_Cursor]["state"] += 1

            if _Tasks[_Cursor]["state"] == 4:
                _Tasks[_Cursor]["state"] = 0

            _Refresh = True
            t.sleep(0.2)
            break

        if k.is_pressed((_OperationKey, "LEFT")):
            _Tasks[_Cursor]["state"] -= 1

            if _Tasks[_Cursor]["state"] == -1:
                _Tasks[_Cursor]["state"] = 3

            _Refresh = True
            t.sleep(0.2)
            break
    return


# New session or continue last one?
while True: 
    cls()
    print(f"""
  {gray}╭─────────{orange}•{end}  Session  {orange}•{gray}─────────╮    
  │                               │  
  │   {red}1.  {orange}Continue last session.  {gray}│
  │   {red}2.  {orange}Create new session.     {gray}│
  │   {red}0.  {red}Exit.                   {gray}│
  │                               │ 
  ╰───────────────────────────────╯{end}  
    """)

    TypeSelection = -1
    while TypeSelection not in range(8):
        TypeSelection = input(f"  {gray}• {orange}")

        try:
            TypeSelection = int(TypeSelection)
        except:
            pass

    if TypeSelection == 0:
        cls()
        exit()

    if TypeSelection == 1:
        try:    

            def TurnToUpper(text):
                def IsNumber(obj):
                    try:
                        int(obj)
                        return True
                    except:
                        return False

                NextUpper = False
                ReadyText = ""
                for symb in list(text):
                    if symb == "%":
                        NextUpper = True
                        continue

                    if NextUpper:
                        NextUpper = False
                        ReadyText += symb.upper()
                        continue

                    if IsNumber(symb) or symb != "%":
                        ReadyText += symb
                    
                    
                return ReadyText
            
            # Convert saved session into dict.
            _Tasks = []

            SavedSessionCP.read(SavedSessionFileLoc)
            SavedList = SavedSessionCP.items("session")

            if SavedList == []:
                print(f"  {red}• Error: No items in saved session.{end}")
                input(f"  {gray}╰ Press enter to continue.{end}")
                TypeSelection = 2

            else:
                for item in SavedList:
                    ReadyItem = TurnToUpper(item[0])
                    _Tasks.append({"state": int(item[1]), "name": ReadyItem})

                break

        except Exception as e:
            print(f"  {red}• Error while trying to read last session. Moving to creating new tasks list process: {e}{end}")
            input(f"  {gray}╰ Press enter to continue.{end}")
            TypeSelection = 2

    if TypeSelection == 2:
        cls()
        print(f"""{gray}
  ╭──────────────{orange}•{end}  Session creation  {orange}•{gray}──────────────╮        
  │                                                  │      
  │  {red}• {orange}Type name of tasks and press enter.           {gray}│      
  │  {red}• {orange}To stop entering process, enter blank input.  {gray}│      
  │                                                  │ 
  ╰──────────────────────────────────────────────────╯{end}  
        """)
        
        SessionCreation_Tasks = []
        _Tasks = []

        # Input tasks.
        while True:
            SessionCreation_NewTask = input(f"  {gray}• {end}")
            if SessionCreation_NewTask == "":
                if SessionCreation_Tasks == []:
                    print(f"{red}  • You cannot continue with blank list.{end}")
                else:
                    break

            elif SessionCreation_NewTask.replace(" ", "") == "":
                continue

            elif SessionCreation_NewTask in SessionCreation_Tasks:
                continue

            else:
                SessionCreation_Tasks.append(SessionCreation_NewTask)
                _Tasks.append({"state": 0, "name": SessionCreation_NewTask})
        break

cls()
_Refresh = True

# Main loop
while True:
    if _Exit:
        print("\n")
        cls()
        exit()

    CursorControl()

    if _Cursor != CursorShadow or _Refresh == True:
        _Refresh = False
        CursorShadow = _Cursor
        cls()

        if _Tasks == []:
            print(f"{gray}Press {_OperationKey} + F5 to add new task.{end}")
            _Cursor = 0
            TaskControl()

        else:
            for i, task in enumerate(_Tasks):
                if task["state"] == 3:
                    print(f"{f'{CursorColorVar}{_CursorChar}{end}' if _Cursor==i else ' '} {gray}[end] | {task['name']}{end}")
                else:
                    stateStr = f"{gray}[ {f'{red}-{end}' if task['state'] == 0 else f'{orange}/{end}' if task['state'] == 1 else f'{green}+{end}' if task['state'] == 2 else ''} {gray}]{end}"
                    print(f"{f'{CursorColorVar}{_CursorChar}{end}' if _Cursor==i else ' '} {stateStr} {gray}| {cyan if i%2==0 else blue}{cyan if not _NamesContrast else ''}{task['name']}{end}")
            
            TaskControl()
