# Import libaries.
from threading import Thread
import socket
import time
import os
import re


# Setup colors.
from modules.colors import *
colors_setup()


# Important switches.
class Important:
    _Prefix    = "@" # @=user | $=admin
    _Username  = "guest"
    _Connected = False


# Minor functions.
def cls(): os.system("cls || clear")
def clearOneLine(line): print(f"\033[1A{' ' * (len(line)+5)}\033[A")
def OutputMesssage(message): print(message)


# Handle messages.
class Messages:
    HEADER = 2048
    FORMAT = "utf-8"
    _welcome_message = ""
    _MessageReceived = False

    class FromServer:
        message_received = "<server:message_received;"
        unknown_command = "<server:unknown_command;"
        user_message = "<server:user_message|"
        connected = "<server:connected;"
        handshake = "<server:handshake;"
        elevate_success = "<server:elevate_succes;"
        elevate_failed = "<server:elevate_failed;" 
        user_degrad = "<server:degrad;"
        welcome_message = "<server:welcome_msg|"

        # Errors.
        admins_limit_error = "<server:admins_limit_error;"
        permissions_error = "<server:permissions_error;"

    class ToServer:
        # Users commands.
        silent_set_username = ">client:silent_username|"
        text_message = ">client:text_message|" 
        disconnect = ">client:disconnect"
        set_username = ">client:username|"
        handshake = ">client:handshake;"
        elevate = ">client:elevate|"
        user_degrad = ">client:degrad;"
        code_2fa = ">client:2fa|"

        # Admin commands.
        ADMIN_server_address = ">client:server_address;"
        ADMIN_server_status = ">client:status;"
        ADMIN_initialize_hs = ">client:iniths;"
        ADMIN_list_clients = ">client:lsusers;"
        
        

    def SendMessage(msg):
        try:
            Socket.sendall(bytes(msg, Messages.FORMAT))

        except ConnectionResetError:
            print(f"{red}SERVER CLOSED!{end}") 
            Menus.Local_informationMessage = "Server has been closed."
            Important._Connected = False
            return



# Server's messages listener.
def ServerMsgListener():
    global Socket
    while True:

        # Receive message from server.
        try:
            ServerMessage = Socket.recv(Messages.HEADER).decode(Messages.FORMAT) 

        # Server closed.
        except ConnectionResetError:
            print(f"{red}[rcv] SERVER CLOSED!{end}") 
            Menus.Local_informationMessage = "Server has been closed."
            Important._Connected = False
            RecreateSocket()
            return
            

        # Commands Queue.
        _CommandsQueue = []
        _CommandsQueue = ServerMessage.split(";")
        _CommandsQueue = [x for x in _CommandsQueue if x]

        # Execute commands.
        if _CommandsQueue != []:
            for command in _CommandsQueue:

                # Server response.
                if command.startswith("<"):

                    # Connection confirmation.
                    if command == Messages.FromServer.connected.replace(";", ""):
                        Important._Connected = True

                    # Welcome message set.
                    if command.startswith(Messages.FromServer.welcome_message):
                        Messages._welcome_message = command.split("|")[1]

                    # Message received confirmation.
                    if command == Messages.FromServer.message_received:
                        Messages._MessageReceived = True

                    # Handshake auth process.
                    if command == Messages.FromServer.handshake.replace(";", ""):
                        Messages.SendMessage(Messages.ToServer.handshake)

                    # Elevate to admin respond : FAILED.
                    if command == Messages.FromServer.elevate_failed.replace(";", ""):
                        OutputMesssage(f"{red}Incorrect admin password.{end}")

                    # Elevate to admin respond : SUCCES.
                    if command == Messages.FromServer.elevate_success.replace(";", ""):
                        OutputMesssage(f"{green}You are now admin.{end}")
                        Important._Prefix = "$"

                    # Permissions degradation.
                    if command == Messages.FromServer.user_degrad:
                        OutputMesssage(f"{red}You are not administrator anymore.{end}")
                        Important._Prefix = "@"

                    # Admin limit reached error.
                    if command == Messages.FromServer.admins_limit_error:
                        OutputMesssage(f"{red} There is maximum amount of admin's.{end}")

                    # Another user message.
                    if command.startswith(Messages.FromServer.user_message):
                        content = command.replace(Messages.FromServer.user_message, "").split("@")
                        prefix  = f"{cyan}@"
                        if len(content) == 1:
                            content = command.replace(Messages.FromServer.user_message, "").split("$")
                            prefix = f"{red}$"

                        message = content[0]
                        username = content[1]
                        OutputMesssage(f"{prefix}{purple}{username}{bold}: {blue}{message}{end}")


                # Server text message.
                else:
                    OutputMesssage(command)


# Handle user input.
def HandleInput(user_input_STR):

    # User commands.
    if user_input_STR.startswith("/"):
        
        # Parse user input.
        user_input = CommandParse(user_input_STR)

        # Disconnect user from server.
        if user_input[0] == "/disconnect":
            Messages.SendMessage(Messages.ToServer.disconnect)     
            print(f"{red}Disconnected.{end}")
            Important._Connected = False
        
        # Change username.
        if user_input[0] == "/setname":
            if len(user_input) != 2:
                print(f"{red}Error:{end} Command <setname> requires exactly 1 parameter: name.")
                return

            username = user_input[1].replace("@","").replace("$", "")

            if len(username) > 24:
                print(f"{red}Error:{end} <setname>: Parameter: name's max lenght is 24 characters!")
                return

            Messages.SendMessage(Messages.ToServer.set_username+username)
            print(f"{cyan}{Important._Prefix}{username}{bold}: {green}New username set!{end}")
            Important._Username = username

        # Become admin.
        if user_input[0] == "/elevate":
            if Important._Prefix == "$":
                print(f"{red}Error:{end} You are already admin!")
                return

            if len(user_input) != 2:
                print(f"{red}Error:{end} Command <elevate> requires exactly 1 parameter: password.")
                return

            Messages.SendMessage(Messages.ToServer.elevate+user_input[1])

        # 2FA code respond.
        if user_input[0] == "/2facode":
            if Important._Prefix == "$":
                print(f"{red}Error:{end} You are already admin!")
                return

            if len(user_input) != 2:
                print(f"{red}Error:{end} Command <2facode> requires exactly 1 parameter: code.")
                return

            Messages.SendMessage(Messages.ToServer.code_2fa+user_input[1])


    # Admin commands.
    elif user_input_STR.startswith(":"):

        # Check if user have admin permissions.
        if Important._Prefix == "@":
            print(f"{red}Error:{end} You cannot use admin commands as user!")
            return

        # Parse user input.
        user_input = CommandParse(user_input_STR)

        # Degrad back to user.
        if user_input[0] == ":deladmin":
            Important._Prefix = "@"
            Messages.SendMessage(Messages.ToServer.user_degrad)
            print(f"{orange}You are not admin anymore.{end}")

        # Get server address.
        if user_input[0] == ":address":
            Messages.SendMessage(Messages.ToServer.ADMIN_server_address)

        # Get objects info.
        if user_input[0] == ":status":
           Messages.SendMessage(Messages.ToServer.ADMIN_server_status)

        # Initialize hs process.
        if user_input[0] == ":iniths":
            Messages.SendMessage(Messages.ToServer.ADMIN_initialize_hs)

        # List clients.
        if user_input[0] == ":lsclients":
            Messages.SendMessage(Messages.ToServer.ADMIN_list_clients)

    # Text message.
    else:
        if not user_input_STR.replace(" ","") == "":
            Messages.SendMessage(Messages.ToServer.text_message+user_input_STR)


# Parse command.
def CommandParse(string):
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


# Connect client to server.
def Connect(host, port):
    global Socket

    try:
        Socket.connect((host, port))
        Thread(target=ServerMsgListener, daemon=True).start()
        time.sleep(0.3)

    except Exception as error:
        error = str(error)

        # Server unactive.
        if "10061" in error:
            error = "Server refused connection."  

        # Not socket.
        if "10038" in error:
            error = "Socket error."

        Menus.Local_informationMessage = error
         

# === Main === #
PORT = 8080 
HOST = "127.0.0.1"
Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def RecreateSocket():
    global Socket
    Socket.close()
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Menus.Local_informationMessage = "Recreated socket."

class Menus:
    Local_informationMessage = ""
    def Local():
        global HOST, PORT, Socket
        output_host, output_port, message = "127.0.0.1", 8080, Menus.Local_informationMessage

        while True:

            cls()
            print(f"""
    {gray}╭────────• {bold}Gchat.{end}
    {gray}│
    {gray}├ {purple}Host{bold}: {red}{output_host}
    {gray}├ {purple}Port{bold}: {red}{output_port}
    {gray}│
    {gray}├ {purple}Name{bold}: {orange}@{Important._Username}{end}
    {gray}├ {red}{message}
    {gray}│""")

            user_action = input(f"    {gray}╰─ {blink}{bold}• {end}")
            user_action_parsed = CommandParse(user_action)
            if len(user_action_parsed) == 0:
                continue

            # Help command.
            if user_action_parsed[0] == "help":
                message = "Commands: connect, resock, help, host, port, exit"

            # Recreate socket.
            if user_action_parsed[0] == "resock":
                RecreateSocket()

            # Connect to server.
            if user_action_parsed[0] in ("connect", "conn", "c"):
                PORT = output_port
                HOST = output_host
      
                Connect(HOST, PORT)
                Menus.Online()
 

            # Exit.
            if user_action_parsed[0] == "exit":
                Socket.close()
                cls()
                exit()
            
            # Change port.
            if user_action_parsed[0] == "port":
                try:
                    output_port = int(user_action_parsed[1])
                    Menus.Local_informationMessage = "Changed port."
                except:
                    Menus.Local_informationMessage = "Invalid port."

            # Change host.
            if user_action_parsed[0] == "host":
                try:
                    output_host = user_action_parsed[1]
                    Menus.Local_informationMessage = "Changed host."
                except:
                    Menus.Local_informationMessage = "Invalid host."

            # Change name.
            if user_action_parsed[0] == "name":
                try:
                    Important._Username = user_action_parsed[1]
                    Menus.Local_informationMessage = "Name changed."
                except:
                    Menus.Local_informationMessage = "Cannot change name."
                  
    def Online():
        cls()
        if Important._Connected:
            Messages.SendMessage(Messages.ToServer.silent_set_username+Important._Username)
            print(f"{green}Connected to server.{end}")
            print(f"{bold}{Messages._welcome_message}{end}")


            while Important._Connected:
                user_input = input("").replace("|", "")
                clearOneLine(user_input)
                HandleInput(user_input)
     
        else:
            RecreateSocket()
                


Menus.Local()
    