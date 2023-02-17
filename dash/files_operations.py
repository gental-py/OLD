def check():
    import os, getpass

    __Validation = False

    try:
        import configparser as cp

    except:
        try:
            os.system("pip install configparser")
            import configparser as cp

        except:
            print("  CriticalError: Cannot import configparser.")
            exit()

    def RegenerateFile(loc):
        os.remove(loc)
        open(loc, "a+")

    _OsUsername_ = getpass.getuser()

    VarsCP = cp.ConfigParser()
    ConfigCP = cp.ConfigParser()
    RegistryCP = cp.ConfigParser()
    CommandsCP   = cp.ConfigParser()

    Logs_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\logs\\"
    Users_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\"
    Online_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\online\\"
    Registry_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\reg.dash"
    MainFolder_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"


    # Does files exists?


    # Main folder
    if not os.path.exists(MainFolder_Loc):
        print("_mainfolder/notexisting_",end="")
        os.mkdir(MainFolder_Loc)

    # Registry
    if not os.path.exists(Registry_Loc) or os.path.getsize(Registry_Loc) == 0:
        print("_registry/notexisting_",end="")
        open(Registry_Loc, "a+").close()
        RegistryCP["reg"] = {"loginNameAsNumber": "false", "checkArgLenght": "true", "spaceAfterCursor": "true", "enableColors": "true", "copyOutput": "false", "showBootupInfo": "false", "enableCustomCommands": "true", "advancedErrorOutput": "false"}
        with open(Registry_Loc, "w") as file:
            RegistryCP.write(file)

    # Users folder
    if not os.path.exists(Users_Loc):
        print("_usersfolder/notexisting_",end="")
        os.mkdir(Users_Loc)

    # Logs folder
    if not os.path.exists(Logs_Loc):
        print("_logsfolder/notexisting_")
        os.mkdir(Logs_Loc)

    # Logs private.log
    if not os.path.exists(Logs_Loc+"private.log"):
        print("_logsprivate/notexisting_")
        open(Logs_Loc+"private.log", "a+")

    # Logs public.log
    if not os.path.exists(Logs_Loc+"public.log"):
        print("_logspublic/notexisting_")
        open(Logs_Loc+"public.log", "a+")

    # Online folder
    if not os.path.exists(Online_Loc):
        print("_online/notexisting_",end="")
        os.mkdir(Online_Loc)

    # Online appdata folder
    if not os.path.exists(Online_Loc+"data\\"):
        print("_online.data/notexisting_",end="")
        os.mkdir(Online_Loc+"data\\")

    # Online appdata/cache folder
    if not os.path.exists(Online_Loc+"data\\cache\\"):
        print("_online.data.cache/notexisting_",end="")
        os.mkdir(Online_Loc+"data\\cache\\")



    # Check files health


    # reg.dash
    try:
        EntriesList = ["loginnameasnumber", "autoupdate", "advancederroroutput", "checkarglenght", "spaceaftercursor", "enablecolors", "copyoutput", "showbootupinfo", "enablecustomcommands"]

        RegistryCP.read(Registry_Loc)
        RegEntries = RegistryCP.items("reg")

        # Checking entries values
        for Entry in RegEntries:

            # Check if entry value is true or false
            if Entry[1] != "true" and Entry[1] != "false":
                print("_registry.nonbooleanvalue_",end="")
                RegistryCP["reg"][Entry[0]] = "false"
                with open(Registry_Loc, "w") as f:
                    RegistryCP.write(f)

            # Check for invalid entry
            if Entry[0] not in EntriesList:
                print(f"_registry.unxcptentry_",end="")
                RegistryCP.remove_option("reg", Entry[0])
                with open(Registry_Loc, "w") as f:
                    RegistryCP.write(f)

        # Check for missing entry
        EntriesNamesList = [RegEntries[x][0] for x in range(len(RegEntries))]
        for mainEntryName in EntriesList:
            if mainEntryName not in EntriesNamesList:
                print(f"_registry.missingentry_",end="")
                RegistryCP["reg"][mainEntryName] = "false"
                with open(Registry_Loc, "w") as f:
                    RegistryCP.write(f)
    except:
        print("_regen.registry_",end="")
        RegenerateFile(Registry_Loc)
        RegistryCP["reg"] = {"autoupdate": "false", "checkArgLenght": "true", "spaceAfterCursor": "true", "enableColors": "true", "copyOutput": "false", "showBootupInfo": "false", "enablecustomcommands": "true", "advancedErrorOutput": "false"}
        with open(Registry_Loc, "w") as file:
            RegistryCP.write(file)

    # Users
    try:
        root_Loc = Users_Loc+"root"
        if not os.path.exists(root_Loc):
            print("_users.rootnotexists_",end="")
            os.mkdir(root_Loc)
        os.system("attrib +h /d " + root_Loc)
    except:
        print("_regen.users_",end="")
        RegenerateFile(Users_Loc)
        if not os.path.exists(root_Loc):
            print("_users.rootnotexists_",end="")
            os.mkdir(root_Loc)
            os.system("attrib +h /d" + root_Loc)
    
    
    # Get all accounts names
    AllAccountsNames = os.listdir(Users_Loc)
    
    for NAME in AllAccountsNames:
        # Configure loop for name
        Vars_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\vars.dash"
        Config_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\config.dash"
        Commands_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\commands.dash"


        # Check if files exists?


        # Vars
        if not os.path.exists(Vars_Loc):
            print(f"_{NAME}.vars/notexists_",end="")
            open(Vars_Loc, "a+")

        # Commands
        if not os.path.exists(Commands_Loc):
            print(f"_{NAME}.commands/notexists_",end="")
            open(Commands_Loc, "a+").close()

        # Config
        if not os.path.exists(Config_Loc) or os.path.getsize(Config_Loc) == 0:
            print(f"_{NAME}.config/notexists_",end="")
            open(Config_Loc, "a+").close()
            ConfigCP["customization"] = {"cursor": ">", "sepchar": ",", "oschar": "."}
            with open(Config_Loc, "w") as file:
                ConfigCP.write(file)

        # Account
        if not os.path.exists(f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\account") or os.path.getsize(f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\account") == 0:
            print(f"_{NAME}_.account/notexists_",end="")
            open(f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\account", "a+")
            if NAME == "root":
                with open(f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\account", "w+") as f:
                    f.write(f"r\nNone.")
            else:
                with open(f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\{NAME}\\account", "w+") as f:
                    f.write(f"u\nNone.")


        # Check files health.


        # vars.dash
        try:
            VarsCP.read(Vars_Loc)
            listOfVariables = VarsCP.sections()
            for Varname in listOfVariables:
                try:
                    var = VarsCP[Varname]["value"]
            
                except:
                    print(f"_vars.incorrectvalue_",end="")
                    vars_open_R = open(Vars_Loc, "r", encoding="utf-8")
                    var_Content = vars_open_R.read()
                    vars_open_R.close()
                    var_Content = var_Content.replace(f"[{Varname}]", "")
                    vars_open_Wp = open(Vars_Loc, "w+", encoding="utf-8")
                    vars_open_Wp.write(var_Content)
                    vars_open_Wp.close()   
        except:
            print(f"_{NAME}.regen/vars_ ",end="")
            RegenerateFile(Vars_Loc)

        # commands.dash
        try:
            CommandsCP.read(Commands_Loc)
            listOfCommands = CommandsCP.sections()
            for CommandName in listOfCommands:
                try:
                    comm = CommandsCP[CommandName]["value"]

                except:
                    print(f"_{NAME}.commands/incorrectvalue_",end="")
                    cmd_open_R = open(Commands_Loc, "r", encoding="utf-8")
                    cmd_Content = cmd_open_R.read()
                    cmd_open_R.close()
                    cmd_Content = cmd_Content.replace(f"[{CommandName}]", "")
                    cmd_open_Wp = open(Commands_Loc, "w+", encoding="utf-8")
                    cmd_open_Wp.write(cmd_Content)
                    cmd_open_Wp.close()              
        except: 
            print(f"_{NAME}.regen/commands_",end="")
            RegenerateFile(Commands_Loc)

        # config.dash
        try:
            ConfigNames = ["cursor", "sepchar", "oschar"]

            ConfigCP.read(Config_Loc, encoding="utf-8")
            CfgItems = ConfigCP.items("customization")

            # Check values
            for Setting in CfgItems:

                # Check for unexcepted settings
                if Setting[0] not in ConfigNames:
                    print(f"_{NAME}.config/unxcptentry_",end="")
                    ConfigCP.remove_option("customization", Setting[0])
                    with open(Config_Loc, "w") as f:
                        ConfigCP.write(f)
                
                # Check for invalid settings values
                try:
                    sttng = Setting[1]
                    if Setting[1].replace(" ","") == "":
                        print(f"_{NAME}.config/wrongvalue_",end="")
                        ConfigCP["customization"][Setting[0]] = "!R"
                        with open(Config_Loc, "w") as f:
                            ConfigCP.write(f)
                except:
                    print(f"_{NAME}.config/wrongvalue_",end="")
                    ConfigCP["customization"][Setting[0]] = "!R"
                    with open(Config_Loc, "w") as f:
                        ConfigCP.write(f)
                
            # Check for missing settings
            ConfigOptions = [CfgItems[x][0] for x in range(len(CfgItems))]
            for mainOption in ConfigNames:
                if mainOption not in ConfigOptions:
                    print(f"_{NAME}.config/missingsetting_",end="")
                    ConfigCP["customization"][mainOption] = "!G"
                    with open(Config_Loc, "w") as f:
                        ConfigCP.write(f)
                        
            # Check if sepchar includes dot.
            if "." in ConfigCP["customization"]["sepchar"]:
                print(f"_{NAME}.config/dotinsepchar_",end="")
                ConfigCP["customization"]["sepchar"] = "!"
                with open(Config_Loc, "w") as f:
                    ConfigCP.write(f)  
        except:
            print(f"_{NAME}.regen/config_",end="")
            RegenerateFile(Config_Loc)
            ConfigCP["customization"] = {"cursor": ">", "sepchar": ",", "oschar": "."}
            with open(Config_Loc, "w") as file:
                ConfigCP.write(file)

    try:
        import install_libaries
    except:
        print("_installlibaries/notfound_")

    __Validation = True
            
    print(f"[Validation: {__Validation}]",end="")


# Recovery user files
def copy_recovery():
    print("  [*] Check files : ",end="")
    check()
    print("OK")

    import os, getpass
    _OsUsername_ = getpass.getuser()

    RCV_Main = f"C:\\Users\\{_OsUsername_}\\Appdata\\LocalLow\\.dash_recovery\\"
    Users_Loc    = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users"
    Main_Loc     = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"

    # Create Main folder
    print("  [*] Check main folder ",end="")
    if not os.path.exists(RCV_Main):
        os.mkdir(RCV_Main)
        print(": Error - Not Exists. : OK")
    else:
        print(": OK")

    # Move files from .dash folder
    print("  [*] Moving all files.")
    if not os.path.exists(Users_Loc):
        print("     -> Skipping - not exists.")

    else:
        try:
            os.system(f"xcopy {Main_Loc} {RCV_Main} /E /C /H /Y")

        except Exception as exc:
            print(f"     -> Error: {exc}")


def paste_recovery():
    import os, getpass

    _OsUsername_ = getpass.getuser()
    RCV_Main = f"C:\\Users\\{_OsUsername_}\\Appdata\\LocalLow\\.dash_recovery\\"
    Main_Folder = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"

    _OsUsername_ = getpass.getuser()
    RCV_Main = f"C:\\Users\\{_OsUsername_}\\Appdata\\LocalLow\\.dash_recovery\\"
    Main_Folder = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\"


    print("  [*] File : reg.dash")
    if not os.path.exists(RCV_Main+"reg.dash"):
        print("  Skipping - not exists.")

    else:
        try:
            os.system(f"copy {RCV_Main}reg.dash {Main_Folder}")

        except Exception as exc:
            print(f"  Error: {exc}")


    print("  [*] Folder : users")
    if not os.path.exists(RCV_Main+"users\\"):
        print("  Skipping - not exists.")
    
    else:
        try:
            os.system(f"xcopy {RCV_Main}users\\ {Main_Folder}users\\ /H /Y /E")
        except Exception as exc:
            print(f"  Error: {exc}")
        
    
    

    
    


def help_commands():
    print("""

    | Command                        | Effect                                     |
    |--------------------------------|--------------------------------------------|
    |     **Basics**                 |                                            |
    | `exit`                         | Exit program.                              |
    | `restart`                      | Restart program.                           |
    | `cls`                          | Clear screen.                              |
    |     **Config**                 |                                            |
    | `mycfg`                        | Display current config.                    |
    | `set.cursor <cursor>`          | Set new cursor.                            |
    | `set.sepchar <sepchar>`        | Set new sepchar.                           |
    | `set.oschar <oschar>`          | Set new system command prefix.             |
    |     **Network**                |                                            |
    | `netinfo`                      | Display your network info.                 |
    | `dnslkp <target.addr>`         | Dns lookup an addres.                      |
    | `revdnslkp <target.ip>`        | Reversed DNS lookup. (ip->addr)            |
    | `ipgeoinfo <target.ip>`        | Returns ip geo location. (Country, city)   |
    | `req.get <response> <url>`     | Make request and return [code/text]        |
    |     **Dash Registry**          |                                            |
    | `dreg.show`                    | Show entries and values.                   |
    | `dreg.edit <entry> <value>`    | Change entry value. [true/false]           |
    | `dreg.copy`                    | Copy current registry code.                |
    | `dreg.paste <code>`            | Paste registry code.                       |
    | `dreg.reset`                   | Reset registry.                            |
    |     **Custom Commands**        |                                            |
    | `<custom.name>`                | Execute custom command.                    |
    | `cstm.add <name>`              | Create custom command.                     |
    | `cstm.open`                    | Open custom commands file.                 |
    | `cstm.convert <mode> <%path>`  | Convert py script to dash. <text/file>     |
    | `cstm.list`                    | Lists all custom commands.                 |
    |     **Variables**              |                                            |
    | `var.list`                     | Lists all variables and their values.      |
    | `var.add <name> <value>`       | Create variable and assign value.          |
    | `var.rem <name>`               | Remove variable.                           |
    | `var.set <name> <value>`       | Assign new value for variable.             |
    |     **Recovery**               |                                            |
    | `rcv.save`                     | Save current user files image.             |
    | `rcv.restore`                  | Restore saved files.                       |
    |     **Accounts (as root)**     |                                            |
    | `acc.create <name> <pass>`     | Create account.                            |
    | `acc.delete <name>`            | Delete account.                            |
    | `acc.chngpasswd <name> <pass>` | Change an account password.                |
    | `acc.logout`                   | Brings you back to login screen.           |
    | `acc.rename <name> <newname>`  | Rename an account.                         |
    | `acc.chngmode <name> <mode>`   | Change an account mode. <root/user>        |
    | `acc.list`                     | Shows list of all accounts.                |
    |     **Accounts (as user)**     |                                            |
    | `acc.chngpasswd <pass> <new>`  | Change current account password.           |
    | `acc.logout`                   | Brings you back to login screen.           |
    | `acc.rename <newname>`         | Change current account name.               |
    | `acc.list`                     | Show list of all accounts.                 |
    |     **Packages**               |                                            |
    | `dget.info <name>`             | Returns informations abaout package.       |
    | `dget.onlinelist`              | Returns all available packages.            |
    | `dget.list`                    | Show all installed packages.               |
    | `dget.get <name>`              | Install package.                           |
    | `dget.remove <name>`           | Remove package.                            |
    |     **Other**                  |                                            |
    | `root`                         | Try to open Dash with root permisions.     |
    | `viewf <path>`                 | Display file with simple highlithing.      |
    | `checkver`                     | Shows local version and check for updates. |
    | `checkfiles`                   | Check program files health.                |
    | `debg.exe <command>`           | Execute command.                           |
               """)

