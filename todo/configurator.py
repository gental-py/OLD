import configparser as cp
import keyboard as k
import time as t
import os 

# Clear screen.
cls = lambda: os.system("cls || clear")

# Colors.
def RepairColors():
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

orange = "\033[0;33m"
purple = "\033[1;35m"
green = "\033[1;32m"
white = "\033[1;37m"
cyan = "\033[1;36m"
gray = "\033[1;30m"
blue = "\033[1;34m"
red = "\033[1;31m"
end = "\033[0m"

# Settings file
SettingsFileLoc = ".\\settings.ini"
config = cp.ConfigParser()

if not os.path.exists(SettingsFileLoc):
    open(SettingsFileLoc, "a+").close() 
    config["settings"] = {"operation_key": "alt", "cursor_color_name": "purple", "wrap_cursor": "0", "names_contrast": "0", "cursor_char": ">"}
    with open(SettingsFileLoc, 'w+') as configuration:
        config.write(configuration)


config.read(SettingsFileLoc)

# Settings
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

except:
    open(SettingsFileLoc, "a+").close() 
    config["settings"] = {"operation_key": "alt", "cursor_color_name": "purple", "wrap_cursor": "0", "names_contrast": "0", "cursor_char": ">"}
    with open(SettingsFileLoc, 'w+') as configuration:
        config.write(configuration)

    config.read(SettingsFileLoc)


# Settings loop
while True:
    cls()
    print(f"{gray}--- {purple}Settings: {gray}---{end}\n")
    print(f"  {gray}1. {cyan}Operation key {gray}: {purple}{_OperationKey}{end}")
    print(f"  {gray}2. {cyan}Cursor color  {gray}: {CursorColorVar}{_CursorColorName.capitalize()}{end}")
    print(f"  {gray}3. {cyan}Wrap cusror   {gray}: {green if _WrapCursor else red}{_WrapCursor}{end}")
    print(f"  {gray}4. {cyan}Names contrast{gray}: {green if _NamesContrast else red}{_NamesContrast}{end}")
    print(f"  {gray}5. {cyan}Cursor char   {gray}: {CursorColorVar}{_CursorChar}{end}\n")
    print(f"  {gray}6. {orange}Repair colors.{end}")
    print(f"  {gray}7. {orange}Go back to main app.{end}")
    print(f"  {gray}0. {red}Exit.\n\n")

    Selection = -1
    while Selection not in range(8):
        Selection = input(f" {gray}>{end}")

        try:
            Selection = int(Selection)
        except:
            pass

    # Exit.
    if Selection == 0:
        exit()

    # Operation key.
    if Selection == 1:
        while True:
            cls()
            print(f"{gray}--- {cyan}Settings: {gray}---{end}")
            print(f"  {gray}Press any key:{end}")

            t.sleep(0.4)
            special_keys = ('alt', 'alt gr', 'ctrl', 'right ctrl', 'shift', 'right shift')
            key_selection_confirmation = True
            key_selection = k.read_key()

            if key_selection not in special_keys:
                print(f"  {red}Warning: {key_selection} is not included in special keys list. It may couse some problems. Do you want to continue?")
                key_selection_acceptation = ''
                key_selection_confirmation = False

                while True:
                    key_selection_acceptation = input(f"  {gray}[{green}Y{gray}/{red}n{gray}] :{end}")
            
                    if key_selection_acceptation.replace(' ','').lower() == 'n':
                        break

                    elif key_selection_acceptation.replace(' ','').lower() == 'y':
                        key_selection_confirmation = True
                        break
                    else:
                        continue
        
            if key_selection_confirmation:
                _OperationKey = key_selection
                config["settings"]["operation_key"] = key_selection
                with open(SettingsFileLoc, 'w') as configfile:
                    config.write(configfile)
                
            break
        continue

    # Cursor color.
    if Selection == 2:
        cls()
        print(f"  {gray}Choose one of those colors:{end}\n")
        
        colors_list = ('orange', 'purple', 'green', 'white', 'cyan', 'gray', 'blue', 'red')
        for i, color in enumerate(colors_list):
            print(f"  {gray}{i+1}.{end} {locals()[color]}{color.capitalize()}{end}")

        while True:
            cursor_color_selection = input(f" {gray}>{end}")
            try:
                cursor_color_selection = int(cursor_color_selection)

                if cursor_color_selection in range(1,9):
                    break

                else:
                    continue

            except:
                continue

        _CursorColorName = colors_list[cursor_color_selection-1]
        CursorColorVar = locals()[_CursorColorName]

        config["settings"]["cursor_color_name"] = _CursorColorName
        with open(SettingsFileLoc, 'w') as configfile:
            config.write(configfile)

    # Wrap cursor.
    if Selection == 3:
        while True:
            cls()
            wrap_cursor_selection = input(f"  {gray}Wrap cursor? [{green}T{gray}/{red}f{gray}] >{end}").replace(' ', '')
            if wrap_cursor_selection.lower() == 't':
                _WrapCursor = True
                break

            elif wrap_cursor_selection.lower() == 'f':
                _WrapCursor = False
                break

            else:
                continue
        
        config["settings"]["wrap_cursor"] = '0' if wrap_cursor_selection.lower() == 'f' else '1'
        with open(SettingsFileLoc, 'w') as configfile:
            config.write(configfile)

    # Names contrast.
    if Selection == 4:
        while True:
            cls()
            names_contrast_selection = input(f"  {gray}Names contrast? [{green}T{gray}/{red}f{gray}] >{end}").replace(' ', '')
            if names_contrast_selection.lower() == 't':
                _NamesContrast = True
                break

            elif names_contrast_selection.lower() == 'f':
                _NamesContrast = False
                break

            else:
                continue
        
        config["settings"]["names_contrast"] = '0' if names_contrast_selection.lower() == 'f' else '1'
        with open(SettingsFileLoc, 'w') as configfile:
            config.write(configfile)

    # Cursor char.
    if Selection == 5:
        while True:
            cls()
            cursor_char_selection = input(f"  {gray}Cursor character:{end}").replace(" ", "")
            if len(cursor_char_selection) == 0:
                continue

            if cursor_char_selection == "%":
                print(f"{red}Character: % cannot be included in cursor.{end}")
                continue

            config["settings"]["cursor_char"] = cursor_char_selection[0]
            _CursorChar = cursor_char_selection[0]
            with open(SettingsFileLoc, 'w') as configuration:
                config.write(configuration)
            break

    # Repair colors.
    if Selection == 6:
        RepairColors()

    # Go back to main app.
    if Selection == 7:
        cls()
        os.system('py todo.py || python3 todo.py || python todo.py')
        exit()