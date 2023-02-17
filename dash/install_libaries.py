
if __import__("platform").system() != "Windows":
    exit()

Packages = ["datetime", "bcrypt", "requests", "getmac", "pyperclip", "configparser"]

def Install(package_name):
    try:
        __import__("os").system(f"pip install {package_name}")
    except:
        print(f"  [ Error ] {package_name} cannot be installed.")

for package in Packages:
    try:
        exec(f"import {package}")
    except:
        try:
            Install(package)
            exec(f"import {package}")
        except:
            print(f"   [ Error ] Cannot import {package}.")