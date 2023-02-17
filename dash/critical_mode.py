def CriticalMode(crash_code="Undefined."):
    import os

    def cls():
        os.system("cls")

    cls()

    def ChooseMenu():
        cls()

        print(f"""    

        < [   Dash Critical Mode   ] >

        Unfortunely, Dash have crashed.


        Crash informations:
            Code = \"{crash_code}\"  
        """)

        print("""
        
        [> Choose menu <]

          0 - Rerun dash.
          1 - Check files automaticly.
          2 - Restore files.
          3 - Download files from github.

        """)

        Choose = input("          >")
        while Choose not in ("0", "1", "2", "3"):
            Choose = input("          >")

        if Choose == "0":
            try:
                os.system("py dash.py")
                exit()
            except Exception as e:
                print(f"        Error: <{e}>")

        if Choose == "1":
            try:
                import files_operations
                files_operations.check()
            except Exception as e:
                print(f"        Error: <{e}>")

        if Choose == "2":
            try:
                import files_operations
                files_operations.paste_recovery()
            except Exception as e:
                print(f"        Error: <{e}>")

        if Choose == "3":
            try:
                import update_code
                exit()
            except Exception as e:
                print(f"        Error: <{e}>")
        
    while True:
        ChooseMenu()

