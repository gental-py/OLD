import threading as t
import socket as s
import time
import os

# Try to import <bcrypt>
try:
    import bcrypt as b

except:
    os.system("pip install bcrypt")
    try:
        import bcrypt as b

    except:
        print(f"[  FATAL ERROR  ] <bcrypt> module cannot be imported.")
        exit()


# Clear screen
cls = lambda: os.system("cls")
cls()


# Colors
end = "\033[0m"
red = "\033[1;31m"
gray = "\033[1;30m"
green = "\033[1;32m"
purple = "\033[1;35m"
yellow = "\033[1;33m"


# Messages
HEADER = 2048
FORMAT = "utf-8"

class Messages:
    class FromServer:
        msg_received = "<server:msg.received;"
        connected = "<server:connected;"
        authorized = "<server:authorized;"
        unauthorized = "<server:unauthorized;"
        handshake = "<server:handshake;"
        admin_elevated = "<server:elevated;"
        admin_notElevated = "<server:not.elevated;"
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


# Important variables
_HandshakeResponse = False
_HandshakeKick = False
_EndOfWatch = False

# Users. (addr[0]&addr[1]) -> 172.26.224.1&12345
_Clients = []
_Admins = []

# Server
PORT = 5050
SERVER = s.gethostbyname(s.gethostname())
ADDRESS = (SERVER, PORT)

server = s.socket(s.AF_INET, s.SOCK_STREAM)
server.bind(ADDRESS)


def Handshaker(connection, addr):
    global _HandshakeKick, _HandshakeResponse

    while True:
        time.sleep(3)
        try:
            connection.send(Messages.FromServer.handshake.encode())
            print("HS: Hand sent.")

        except Exception as e:
            print(f"{gray}[{purple}SERVER{gray}:{yellow}Handshaker{gray}] {addr[0]}:{addr[1]} {red}Kicked client due error: {e}{end}.")
            _HandshakeKick = True
            connection.close()
            return

        time.sleep(3)

        if _HandshakeResponse:
            _HandshakeResponse = False
        else:
            print(f"{gray}[{purple}SERVER{gray}:{yellow}Handshaker{gray}] {addr[0]}:{addr[1]} {red}Kicked client for no response{end}.")
            _HandshakeKick = True
            connection.close()
            return


def HandleClient(connection, addr):
    global thread, server, _Admins, _Clients, SERVER, PORT, _EndOfWatch, _HandshakeKick, _HandshakeResponse

    handshaker_thread = t.Thread(target=Handshaker, args=(connection,addr))
    handshaker_thread.start()

    try:

        # Send connection confirmation.
        connection.send(Messages.FromServer.connected.encode())
        print(f"{gray}[{end}client{gray}@{yellow}{addr[0]}{gray}:{yellow}{addr[1]}{gray}]{end} {green}Connected to server.{end}")
        

        # Authorize client.
        _authorizeClient = False

        #    + Check if IP adrres is the same.
        if addr[0].split(".")[0]+addr[0].split(".")[1] in SERVER.replace(".",""):
            _authorizeClient = True

        if _authorizeClient:
            connection.send(Messages.FromServer.authorized.encode())
            print(f"{gray}[{end}client{gray}@{yellow}{addr[0]}{gray}:{yellow}{addr[1]}{gray}]{end} {green}User authorized.{end}")
            _Clients.append(f"{addr[0]}&{addr[1]}")

        else:
            connection.send(Messages.FromServer.unauthorized.encode())
            print(f"{gray}[{end}client{gray}@{yellow}{addr[0]}{gray}:{yellow}{addr[1]}{gray}]{end} {red}User unauthorized.{end}")
            connection.close()


        client_IsAdmin = False
        connected = True
        while connected:

            if _HandshakeKick:
                connection.close()
                connected = False

            msg_lenght = connection.recv(HEADER).decode(FORMAT)

            if msg_lenght:

                connection.send(Messages.FromServer.msg_received.encode())
                msg_lenght = int(msg_lenght)
                MESSAGE = connection.recv(msg_lenght).decode(FORMAT)

                # Commands (client permissions).
                if MESSAGE == Messages.ToServer.disconnect:
                    print(f"{gray}[{end}{f'{red}*admin' if client_IsAdmin else 'client'}{gray}@{yellow}{addr[0]}{gray}:{yellow}{addr[1]}{gray}]{end} {red}Disconnected.{end}")
                    if client_IsAdmin:
                        _Admins.remove(f"{addr[0]}&{addr[1]}")
                        client_IsAdmin = False

                    if f"{addr[0]}&{addr[1]}" in _Clients: _Clients.remove(f"{addr[0]}&{addr[1]}") 
                    connected = False

                # Handshake.
                elif MESSAGE == Messages.ToServer.handshake:
                    print("HS: response received")
                    _HandshakeResponse = True

                # !ping
                elif MESSAGE == Messages.ToServer.connection_test:
                    connection.send("Pong!".encode())
  
                elif MESSAGE.startswith(Messages.ToServer.elevate):
                    if b.checkpw(MESSAGE.split("|")[1].encode(), b'$2b$05$CqYzGroOOiPFioPJFMmGIeWp6cEeklL3n17/mDMop0erPoiku9MSK'):
                        _Admins.append(f"{addr[0]}&{addr[1]}")
                        client_IsAdmin = True
                        connection.send(Messages.FromServer.admin_elevated.encode())
                        print(f"{gray}[{purple}SERVER{gray}:{yellow}Administrators{gray}]{end} {red}*{end}{addr[1]} become {red}Administrator{end}.")

                    else:
                        connection.send(Messages.FromServer.admin_notElevated.encode())
                        print(f"{gray}[{purple}SERVER{gray}:{yellow}Administrators{gray}]{end} {red}{addr[1]} unsuccesfully tried to elevate to Administrator{end}.")


                # Commands (as administrator).

                # !degrad
                elif MESSAGE == Messages.ToServer.degrad:
                    if client_IsAdmin:
                        print(f"{gray}[{purple}SERVER{gray}:{yellow}Administrators{gray}]{end} {red}{addr[1]} Administrator degraded himself{end}.")
                        _Admins.remove(addr[1])
                        client_IsAdmin = False

                    else:
                        connection.send("You are not Administrator!".encode())

                # !getaddr
                elif MESSAGE == Messages.ToServer.admin_getaddr:
                    if client_IsAdmin:
                        connection.send(f"Address: {SERVER}:{PORT}".encode())

                    else:
                        connection.send("You are not Administrator!".encode())

                # !getactiveconn
                elif MESSAGE == Messages.ToServer.admin_getactive_connections:
                    if client_IsAdmin:
                        msg_clients = "\n".join(client.replace("&", ":") for client in _Clients if client not in _Admins)
                        msg_admins  = "\n".join("*"+admin.replace("&", ":") for admin in _Admins) 
                        msg_conns = Messages.FromServer.admin_active_connections + f" --@ Clients: {len(_Clients)}--\n" + msg_clients + "\n" + msg_admins + " "
        
                        connection.send(msg_conns.encode())

                    else:
                        connection.send("You are not Administrator!".encode())

                # !close_server
                elif MESSAGE.startswith(Messages.ToServer.admin_close_server):
                    if b.checkpw(MESSAGE.split("|")[1].encode(), b'$2b$05$W7KuVc/E2QDlCHcGGvSJne/mN3DUWnoxZ8t8L/dZxXS1BT6EJmmdO'):
                        print(f"{gray}====== {red}END OF SERVICE.{end} {gray}======{end}\n")
                        server.close()
                        _EndOfWatch = True
                        return False

                    else:
                        connection.send(Messages.FromServer.admin_notElevated.encode())
                        print(f"{gray}[{purple}SERVER{gray}:{yellow}Administrators{gray}]{end} {red}{addr[1]} unsuccesfully tried to elevate to Administrator{end}.")


                # User message. Not command.
                else:
                    if client_IsAdmin:
                        print(f"{gray}[{red}*admin{gray}@{yellow}{addr[0]}{gray}:{yellow}{addr[1]}{gray}]{end} {MESSAGE.replace('_', ' ')}")
                    else:
                        print(f"{gray}[{end}client{gray}@{yellow}{addr[0]}{gray}:{yellow}{addr[1]}{gray}]{end} {MESSAGE.replace('_', ' ')}")

        if f"{addr[0]}&{addr[1]}" in _Clients: _Clients.remove(f"{addr[0]}&{addr[1]}") 
        connection.close()

    except Exception as e:
        # When user quit without closing connection.
        if "10054" in str(e):
            if f"{addr[0]}&{addr[1]}" in _Clients: _Clients.remove(f"{addr[0]}&{addr[1]}") 
            connection.close()
            print(f"{gray}[{purple}SERVER{gray}:{yellow}ClientHandler:{red}ERROR{gray}]{end} Manually closed connection because client left without closing it.")
            return False

        print(f"{gray}[{purple}SERVER{gray}:{yellow}ClientHandler:{red}ERROR{gray}]{end} Error: {e}")


def Start():
    global _EndOfWatch, thread
    if _EndOfWatch:
        exit()

    server.listen()
    print(f"{gray}[{purple}SERVER{gray}:{yellow}Listener{gray}]{end} Server is listening on: {gray}{SERVER} {end}: {gray}{PORT}{end}")
    
    while True:
        if _EndOfWatch:
            exit()

        conn, addr = server.accept()
        thread = t.Thread(target=HandleClient, args=(conn,addr))
        thread.start()


print(f"{gray}====== {green}SERVER STARTED{end} {gray}======{end}\n")
Start()
