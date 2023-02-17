import threading as t
import getpass as gp
import socket as s
import time 
import os

# Clear screen.
cls = lambda: os.system("cls")
cls()

# Colors.
end = "\033[0m"
red = "\033[1;31m"
gray = "\033[1;30m"
green = "\033[1;32m"
purple = "\033[1;35m"
yellow = "\033[1;33m"

# ------ Messages: ------ #

# Important variables for messages.
HEADER = 2048
FORMAT = "utf-8"

class Messages:
    class FromServer:
        msg_received = "<server:msg.received"
        connected = "<server:connected"
        authorized = "<server:authorized"
        unauthorized = "<server:unauthorized"
        handshake = "<server:handshake"
        admin_elevated = "<server:elevated"
        admin_notElevated = "<server:not.elevated"
        admin_addr = "<server:address|"
        admin_active_connections = "<server:active.connections|"
        server_closed = "<server:server_closed"

    class ToServer:
        connection_test = ">client:connection.test"
        disconnect = ">client:disconnect"
        elevate = ">client:elevate.admin|"
        degrad = ">client:degrad.admin"
        handshake = ">client:handshake"
        admin_getaddr = ">admin:get.addr"
        admin_getactive_connections = ">admin:active.connections"
        admin_close_server = ">admin:close.server|"
        

# Receive message function.
def ReceiveMessage():
    try:
        global _messageReceived, _escapeServer, _exit

        # Receive message from server.
        _MessageFromServer = client.recv(HEADER).decode(FORMAT)  

        # Commands Queue
        _CommandsQueue = []
        _CommandsQueue = _MessageFromServer.split(";")
        _CommandsQueue = [x for x in _CommandsQueue if x]


        if _CommandsQueue != []:
            for command in _CommandsQueue:

                if command.startswith("<"):

                    # Confirm connection.
                    if command == Messages.FromServer.connected:
                        ConnectionProcessStates.connectionState = True
                    
                    # Authorize client.
                    elif command == Messages.FromServer.authorized:
                        ConnectionProcessStates.authorizationState = True

                    elif command == Messages.FromServer.unauthorized:
                        ConnectionProcessStates.authorizationState = False

                    # Confirm message receipt.
                    elif command == Messages.FromServer.msg_received:
                        _messageReceived = True

                    # Handshake response.
                    elif command == Messages.FromServer.handshake:
                        print("Handshake sent back.\n")
                        SendMessage(Messages.ToServer.handshake)

                    # Server closed.
                    elif command == Messages.FromServer.server_closed:
                        _escapeServer = True
                        _exit = True
                        print(f"{gray}[{purple}SERVER{gray}]{red} Server closed by Administrator{end}.")
                        client.close()

                    # Elevate to admin.
                    elif command == Messages.FromServer.admin_elevated:
                        print(f"{gray}[{purple}SERVER{gray}]{end} {green}Succesfully elevated to {red}Administrator{end}.")

                    elif command == Messages.FromServer.admin_notElevated:
                        print(f"{gray}[{purple}SERVER{gray}]{end} {red}Unsuccesfully tried to elevate to Administrator{end}.")

                    # Active connections.
                    elif command.startswith(Messages.FromServer.admin_active_connections):
                        conns_List = command.split("|")
                        conns_List.pop(0)
                        clients_List = conns_List[0]

                        print("\n", clients_List.replace("--",f"{gray}--{end}").replace("*",f"{red}*{end}"))
                        print(end)


                    # Unrecognizable server command.
                    else:
                        print(f"{gray}[{purple}SERVER{gray}:{red}Unrecognizable{yellow}Message{gray}]{end} {command}")
                
                # Non-command message from server.
                else:
                    print(f"{gray}[{purple}SERVER{gray}:{yellow}Message{gray}]{end} {command}")
    
        _CommandsQueue = []

    except Exception as e:
        # Disconnect if server has been unexceptly closed.
        if "10054" in str(e):
            print(f"{gray}[{red}ERROR{gray}]{end} (RM) Server has been unexceptly closen.")
            _messageReceived = False
            _escapeServer = True

            return

        # In other case just print error.
        else:
            print(f"\n{gray}[{red}ERROR{gray}]{end} Unexcepted error has ocured: {e}")

# Send message to server function.
def SendMessage(msg):  
    try: 
        global _exit

        # Check if message is not blank.
        if not msg.replace(" ","") == "":         
            msg = msg.replace(" ","_")

            # Disconnect from server.
            if msg == "!disconnect" or msg == Messages.ToServer.disconnect:
                msg = Messages.ToServer.disconnect
                _exit = True

            # Send test message to server.
            if msg == "!ping" or msg == Messages.ToServer.connection_test:
                msg = Messages.ToServer.connection_test

            # Change client mode.
            if msg == "!degrad" or msg == Messages.ToServer.degrad:
                msg = Messages.ToServer.degrad

            if msg == "!elevate" or msg == Messages.ToServer.elevate:
                msg = Messages.ToServer.elevate
                msg_elevate_password = gp.getpass(f"{gray}[{yellow}?{gray}]{end} Password: {gray}", stream="*")
                msg += msg_elevate_password
           
           # Admin commands.
            if msg == "!getaddr" or msg == Messages.ToServer.admin_getaddr:
                msg = Messages.ToServer.admin_getaddr

            if msg == "!getactiveconn" or msg == Messages.ToServer.admin_getactive_connections:
                msg = Messages.ToServer.admin_getactive_connections

            if msg == "!close_server" or msg == Messages.ToServer.admin_close_server:
                msg = Messages.ToServer.admin_close_server
                msg_closeSV_password = gp.getpass(f"{gray}[{yellow}?{gray}]{end} Password: {gray}", stream="*")
                msg += msg_closeSV_password

            try:
                # Ready up message to send.
                message = msg.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length += b' ' * (HEADER - len(send_length))
                
                # Send message.
                client.send(send_length)
                client.send(message)

                # Delay sending multiple messages at once.
                time.sleep(0.2)

                return True

            except Exception as e:
                # Error while sending message.
                print(f"{gray}[{red}ERROR{gray}]{end} Cannot send message. Error: {e}")
                return False

        return

    except Exception as e:
        # Unexcepted error.
        print(f"{gray}[{red}ERROR{gray}]{end} Unexcepted error has ocured: {e}")
        LocalMode()


# ------ Server: ------ #

# States switches of connection process.
class ConnectionProcessStates:
    connectionState = False
    authorizationState = bool

# Important switches.
_messageReceived = False
_escapeServer = False
_exit = False

# Create socket.
client = s.socket(s.AF_INET, s.SOCK_STREAM)


# Recreate socket to avoid errors.
def RecreateSocket():
    global client
    client.close()
    client = s.socket(s.AF_INET, s.SOCK_STREAM)
    print(f"{gray}[{yellow}SOCKET{gray}]{end} Restarted socket connection.")

# Connect to server.
def Connect(server, port):
    try:
        # Make a connection with server.
        ADDR = (server, port)
        client.connect(ADDR)

        # Wait for server response.
        receiver = t.Thread(target=ReceiveMessage)
        receiver.start()
        print(f"{gray}[{purple}SYSTEM{gray}]{green} Connected {gray}~ {end}",end="")
        
        time.sleep(0.5)

        # Wait for authenticate client.
        receiver = t.Thread(target=ReceiveMessage)
        receiver.start()

        time.sleep(0.5)

        # [v] Authorized.
        if ConnectionProcessStates.authorizationState == True:    
            print(f"{green}Authorized.{end}")
            return True

        # [x] Blocked.
        elif ConnectionProcessStates.authorizationState == False:
            print(f"{red}Unauthorized.{end}")
            return False

        # [-] Not caught.
        else:
            print(f"{red}Not caught.{end}")
            return False

    except Exception as e1:
        # Try to repair error in case when socket is actually logged.
        if "10056" in str(e1):
            RecreateSocket()

            try:
                # Make a connection with server.
                ADDR = (server, port)
                client.connect(ADDR)

                # Wait for server response.
                receiver = t.Thread(target=ReceiveMessage)
                receiver.start()
                print(f"{gray}[{purple}SYSTEM{gray}]{green} Connected {gray}~ {end}",end="")
                
                time.sleep(1)

                # Wait for authenticate client.
                receiver = t.Thread(target=ReceiveMessage)
                receiver.start()

                time.sleep(1)

                # [v] Authorized.
                if ConnectionProcessStates.authorizationState == True:    
                    print(f"{green}Authorized.{end}")
                    return True

                # [x] Blocked.
                elif ConnectionProcessStates.authorizationState == False:
                    print(f"{red}Unauthorized.{end}")
                    return False

                # [-] Not caught.
                else:
                    print(f"{red}Not caught.{end}")
                    return False
        
            except Exception as e2:
                print(f"{gray}[{purple}SYSTEM{gray}]{red} Cannot connect. Error: {end}{e2}")

        print(f"{gray}[{purple}SYSTEM{gray}]{red} Cannot connect. Error: {end}{e1}")
        return False


# ------ Modes: ------ #

def LocalMode():
    
    print(f"\n\n{gray}---{yellow} Local {gray}---{end}\n")

    while True:
        # Ask for server IP.
        _ConnectionIP = input(f"\n{gray}[{yellow}?{gray}]{end} Server IP: {gray}")

        if _ConnectionIP.startswith("#"):
            _ConnectionIP = _ConnectionIP.replace("#","",1)
            _ConnectionIP = "172.26.224.1"

        if _ConnectionIP.replace(" ", "") == "resock":
            RecreateSocket()
            continue

        if _ConnectionIP.replace(" ","") == "exit":
            print(end)
            exit()


        # Ask for server PORT.
        _ConnectionPORT = input(f"{gray}[{yellow}?{gray}]{end} Server PORT: {gray}")
        
        if _ConnectionPORT.startswith("#"):
            _ConnectionPORT = _ConnectionPORT.replace("#","",1)
            _ConnectionPORT = 5050

        try: 
            _ConnectionPORT = int(_ConnectionPORT)

        except: 
            print(f"{gray}[{red}ERROR{gray}] {red}Port is not a number.{end}\n")
            continue

        # Try to connect to server.
        ConnectionStatus = Connect(_ConnectionIP, _ConnectionPORT)

        # If connection is correct.
        if ConnectionStatus == True:
            PublicMode()

        # Otherwise ask for ip and port again.
        else:
            continue

def PublicMode():
    try:
        global _exit, _escapeServer
        ClientCommandsList = ["!disconnect", "!ping", "!elevate"]
        AdminCommandsList = ["!close_server", "!kick", "!degrad", "!getaddr", "!getactiveconn"]

        print(f"\n\n{gray}---{purple} Public {gray}---{end}\n\n")
        
        while True:
            # Check if escaping server protocol is turned on.
            if _escapeServer:
                _escapeServer = False
                break
            
            # Check if exiting server protocol is turned on.
            if _exit == True:
                _exit = False
                LocalMode()

            # Receive messages on other thread.
            receiver = t.Thread(target=ReceiveMessage)
            receiver.start()

            # Ask for command/message.
            PublicCommand = input(f"{gray}>{end} ")

            try:
                # Check if message is command.
                if PublicCommand.startswith("!"):
                    PublicCommand = PublicCommand.replace(" ", "")

                if PublicCommand.startswith("!") and PublicCommand not in ClientCommandsList and PublicCommand.startswith("!") and PublicCommand not in AdminCommandsList:
                    print(f"{gray}[{red}ERROR{gray}]{end} Unrecognizable command.")

                # Send message.
                else:
                    SendMessage(PublicCommand)

            # Unexcepted error while sending message.
            except Exception as e:
                print(f"{gray}[{red}ERROR{gray}]{end} {e}")
                RecreateSocket()
                LocalMode()

    # Unexcepted error while sending message process ocure an error.
    except Exception as e:
        print(f"{gray}[{red}ERROR{gray}]{end} Unexcepted error has ocured: {e}")
        RecreateSocket() 
        LocalMode()
        
    LocalMode()
        

# ------ Main: ------ #

# Start session.
print(f"{gray}====== {green}SESSION STARTED {gray}======{end}")
LocalMode()
