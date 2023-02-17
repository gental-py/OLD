import os

try:
    import requests

except:
    try:
        os.system("pip install requests")
        import requests
    except:
        print("  Cannot import requests.")
        exit()

scriptRootURL = r"https://raw.githubusercontent.com/GentalYT/dash/main/"
cfg = ["dget.py", "accounts.py", "dash.py", "files_operations.py", "critical_mode.py", "install_libaries.py"]

for name in cfg:
    try:
        with open(name, "w", encoding="utf-8") as f:
            f.write(requests.get(scriptRootURL + name).text.replace("\n",""))
    except Exception as e:
        print(f"  Error: Cannot install file: {name}\nException: {e}")

print("  Installed update.")
import dash