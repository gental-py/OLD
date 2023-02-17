import requests as req
import os, getpass


# Set state variables
_OsUsername_ = getpass.getuser()
Online_Loc = f"C:\\Users\\{_OsUsername_}\\Appdata\\Local\\.dash\\online\\"
Online_URL = "https://raw.githubusercontent.com/gental-py/dash/dget_db/online/"


# Check if <online> exists
if not os.path.exists(Online_Loc):
    os.mkdir(Online_Loc)


# Program control
def CheckIfModuleExists(name):
    Modules = GlobalList()
    if name in Modules:
        return True
    else:
        return False


# User control
def Info(name):
    if CheckIfModuleExists(name) == True:
        FileContent = req.get(Online_URL+name+".py").text

        FileContent = FileContent.split("\n")
        if "#<" in FileContent[0] and ">#" in FileContent[0]:
            DescriptionLine = FileContent[0]
        else:
            return "None"

        return DescriptionLine.replace("#<", "").replace(">#", "")

    else:
        return False

def GlobalList():
    try:
        Request = req.get(Online_URL + "list").text
    except Exception as e:
        return f"Error: {e}"

    try:
        Request = Request.replace("\n","")
        NamesList = Request.split(",")
    except Exception as e:
        return f"Error: {e}"

    return NamesList

def LocalList():
    Files = os.listdir(Online_Loc)
    Modules = []
    for file in Files:
        if file.endswith(".py"):
            Modules.append(file.replace(".py",""))

    return Modules

def Install(name):
    if CheckIfModuleExists(name):
        if not os.path.exists(Online_Loc+name+".py"):
            print(f"  [*] Created file: {Online_Loc+name+'.py'}")
            open(Online_Loc+name+".py", "a+")

        else:
            print("  Module already satisfied. Overwrite it?")
            Ask = input("  [y/n] > ")
            while Ask.lower().replace(" ","") not in ("y","n"):
                Ask = input("  [y/n] > ")

            if Ask == "n":
                return "  Module already satisfied, and user cancel overwritting operation."
            
        print(f"  [*] Creating request to: <{name}.py>.")
        request_CodeFile = req.get(Online_URL+name+".py")
        OnlineFileContent = request_CodeFile.text
        request_Code = request_CodeFile.status_code

        print(f"  [*] Server responsed.")
        print(f"  [*] Response code: ({request_Code})")
        if request_Code != 200:
            return f"  Server response code is not 200. ({request_Code})"

        print(f"  [*] Writing file.")

        FileContent_Split = OnlineFileContent.split("\n")
        with open(Online_Loc+name+".py", "w+") as f:
            for line in FileContent_Split:
                if line != "\n":
                    f.write(line+"\n")

        print(f"  [*] Online code writted to local file.")
        return True

    else:
        return "  Module not found."

def Remove(name):
    if not os.path.exists(Online_Loc+name+".py"):
        return "  Module not found."

    else:
        try:
            os.remove(Online_Loc+name+".py")
            print("  [*] Removed.")
            return True

        except Exception as e:
            return f"  Cannot delete file: <{e}>"

