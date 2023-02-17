try:
    import os, getpass, bcrypt

except:
    try:
        import critical_mode
        critical_mode.CriticalMode("Error while trying to import <bcrpyt> [accounts]")
    except:
        print("Critical error...")
        exit()

_OsUsername_ = getpass.getuser()
Users_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\users\\" 

# Program control
def CheckIfNameExists(name):
    if name.replace(" ","") == "":
        return False

    if os.path.exists(Users_Loc+name):
        return True
    else:
        return False

def UserInfo(name):
    AccountPath = Users_Loc+name+"\\account"
    AccFileContent = open(AccountPath, "r").readlines()
    AccountPermisions = AccFileContent[0]
    AccountPassword = AccFileContent[1]
    return (AccountPassword, AccountPermisions) 


# User control
def create(name, password):
    if CheckIfNameExists(name) == False:
        os.mkdir(Users_Loc + name)

        # create user files
        AccountPath = Users_Loc+name+"\\"
        NewUserFileContent = f"u\n{password}"
        open(AccountPath+"account", "a+")
        open(AccountPath+f"account", "w+").write(NewUserFileContent)
        open(AccountPath+"vars.dash", "a+").close()
        open(AccountPath+"config.dash", "a+").close()
        open(AccountPath+"commands.dash", "a+").close()
     
        return "Account created."

    else:
        return f"Account named {name} already exists."

def delete(name):
    if CheckIfNameExists(name):
        try:
            backslash = "\\"
            os.system(f"rmdir /Q /S {Users_Loc+name+backslash}")
            return True

        except Exception as e:
            return f"Error. {e}"
    else:
        return "Account does not exists."

def login(name, password):
    if CheckIfNameExists(name) == True:
        try:
            AccountPassword = UserInfo(name)[0].replace("b", "", 1).replace("'", "", 1)[:-1]
        except Exception as e:
            return f"Error: Cannot fetch account password. <{e}>"

        login_status = bcrypt.checkpw(bytes(password.encode()), bytes(AccountPassword.encode()))
        if login_status == True:
            return True
        else:
            return "Wrong password."

    else:
        return f"No account named: \"{name}\""

def change_pass(name, current_password, new_password):
    AccountPath = Users_Loc+name+"\\"
    AccountPermissions = UserInfo(name)[1].replace(" ","")
    AccountPassword = UserInfo(name)[0].replace("b", "", 1).replace("'", "", 1)[:-1]
    
    if current_password != "SKIPPED_BECOUSE_COMMAND_TYPED_BY_ROOT":
        if bcrypt.checkpw(bytes(current_password.encode()), bytes(AccountPassword.encode())) != True:
            return "Incorrect password."
    
    try:
        NewFileContent = AccountPermissions+str(new_password)
        with open(AccountPath+"account", "w+") as file:
            file.write(NewFileContent)
        return True

    except Exception as e:
        return e
      
def check_root_password():
    root_hashed = UserInfo("root")[0].replace("b", "", 1).replace("'", "", 1)[:-1]

    for i in range(3):
        given_Password = getpass.getpass(f"  ({i+1}/{3}) Enter [root] password: ")

        if bcrypt.checkpw(bytes(given_Password.encode()), bytes(root_hashed.encode())):
            return True

    return False

def setup_root():
    print("  [Root] account is not set up.\n  Create password for [root] account.")
    password = getpass.getpass("  Password : ")
    hashed_pw = bcrypt.hashpw(bytes(password.encode()), bytes(bcrypt.gensalt()))
    file_content = f"r\n{hashed_pw}"
    with open(Users_Loc+"root\\account", "w+") as f:
        f.write(file_content)

def rename(account, newname):
    if CheckIfNameExists(account) == True:
        CurrentAccountPath = Users_Loc+account+"\\"
        NewAccountPath = Users_Loc+newname+"\\"
        try:
            os.rename(CurrentAccountPath, NewAccountPath)
            return True
        except Exception as e:
            return f"Error: <{e}>"

    else:
        return f"No account named: \"{account}\""

def change_mode(name, mode):
    if CheckIfNameExists(name) == True:
        AccountPath = Users_Loc+name+"\\account"

        # Save password
        account_password = UserInfo(name)[0]

        file_content = mode+"\n"+account_password
        with open(AccountPath, "w+") as f:
            f.write(file_content)

        return True
    else:
        return f"No account named: \"{name}\""

def list_accounts():
    ROOTS = []
    USERS = []

    allAccounts = os.listdir(Users_Loc)

    for dir in allAccounts:
        if "u" in UserInfo(dir)[1]:
            USERS.append(dir)

        elif "r" in UserInfo(dir)[1]:
            ROOTS.append(dir)

        else:
            print(f"  <an error with: {dir}>")

    return(USERS, ROOTS)


    
