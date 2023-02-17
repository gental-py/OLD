def help():
    RED = "\033[0;31m"
    BLUE = "\033[0;34m"
    LIGHT_RED = "\033[1;31m"
    CYAN = "\033[0;36m"
    LIGHT_CYAN = "\033[1;36m"

    print(f"{BLUE}==== {LIGHT_RED}HELP {BLUE}====")
    print(f"\n{LIGHT_RED}EXIT {CYAN}= Exit program.")
    print(f"\n{LIGHT_RED}RESTART {CYAN}= Restart program.")
    print(f"\n{LIGHT_RED}SAY {CYAN}= Outputting text, that you have typed.{LIGHT_CYAN}\n> Type <--a> to make text look like T H I S.")
    print(f"\n{LIGHT_RED}CLS {CYAN}= Clear screen.")
    print(f"\n{LIGHT_RED}STATUS {CYAN}= Shows informations abauot program and files.{LIGHT_CYAN}\n> Startup label is showing how does files start. If number is 0, file is working, if 1, file is corrupted.\n - 1. number = Main folder.\n - 2. number = File with name\n - 3. number = File with logs\n - 4. number = File with theme\n\n> Sizes label is showing how big is files.\n - 1. number = Main foler.\n - 2. number = File with name\n - 3. number = File with logs\n - 4. number = Main file\n\n> Version label shows version of program\n\n> Name label shows your username.")
    print(f"\n{LIGHT_RED}CHNGNAME {CYAN}= Change your username.")
    print(f"\n{LIGHT_RED}DATE {CYAN}= Outputting actual date.")
    print(f"\n{LIGHT_RED}TIME {CYAN}= Outputting actual time.")
    print(f"\n{LIGHT_RED}LOG {CYAN}= Clear / show log file size.\n> -size = Shows size of file.\n> -clr = Clears logs file.\n> -show = Shows all logs.")
    print(f"\n{LIGHT_RED}PCINFO {CYAN}= Outputting informations about your PC.\n> Available attributes: -cpu -gpu -ram -net -disk // -all")
    print(f"\n{LIGHT_RED}VERCHECK {CYAN}= Check program version for updates.")
    print(f"\n{LIGHT_RED}THEMES {CYAN}= Shows all available themes.")
    print(f"\n{LIGHT_RED}SETTHEME {CYAN}= Change theme for one in THEMES list.")
    print(f"\n{LIGHT_RED}TESTNET {CYAN}= Shows upload and download speed, also your ping.")
    print(f"\n{LIGHT_RED}WEBSEARCH {CYAN}= Search phrase in google.")
    print(f"\n{LIGHT_RED}WEBOPEN {CYAN}= Open url in browser.")
