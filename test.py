import argparse
import sys, os
import threading
import socket

arguments_size = len(sys.argv)
arguments = sys.argv
global my_port
global my_server_port
global my_server
global servers

#reading topology file
def readFile(path):
    global servers
    servers = []
    print("Reading file...")
    topologyStr = []
    with open(path) as my_file:
        for line in my_file:
            temp = line.split()
            if len(temp) > 2 and  temp[1].find('.') !=-1:
                servers.append(line)
            topologyStr.append(line)
    print("File read")
    global my_server_port
    temp = topologyStr[2].split()
    my_server_port = int(temp[2])

#Error message for invalid server command
def serverError():
    print("Missing arguments to start the program.")
    print("Use the following template:")
    print("server -t  <topology-file-name> -i <routing-update-interval>")
    print("Program terminated")


#funtion to start the server
def server():
    print("Server started at port: ",my_server_port)
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    global my_server
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_server:
        my_server.bind((HOST, my_server_port))
        #waiting to receive any message
        while True:
            data, address = my_server.recvfrom(1024)
            print('\nreceived {} bytes from {}'.format(len(data), address))
            print(data.decode())
            print("Waiting for command: ")

#update function
def update():
    print("Update option")

#step function
def step():
    for s in servers:
        temp = s.split()
        HOST = temp[1]              # The server's hostname or IP address
        PORT = int(temp[2])         # The port used by the server
        my_mgs = str.encode("This is a routing update.")
        my_server.sendto(my_mgs, (HOST, PORT))
    print("Routing update completed")

#packets function
def packets():
    print("Packets option")

#display function
def display():
    print("Display option")

#disable function
def disable():
    print("Disable option")

#crash function
def crash():
    print("Crash option")
    
# main menu function
def mainMenu():
    print("You can enter a command at any time")
    temp = ''
    while temp != 'exit' :
        val = input("Waiting for command: ")
        splitCommand = val.split()
        if len(splitCommand) > 0 :
            if splitCommand[0] == 'update':
                if len(splitCommand) > 3 :
                    update()
                else:
                    print("Missing arguments")
                    print("Use the following template:")
                    print("update <server-ID1> <server-ID2> <Link Cost>")
            elif splitCommand[0] == "step":
                step()
            elif splitCommand[0] == "packets":
                packets()
            elif splitCommand[0] == "display":
                display()
            elif splitCommand[0] == "disable":
                if len(splitCommand) > 1 :
                    if splitCommand[1].isnumeric() :
                        disable()
                    else:
                        print("Enter a number for server ID")
                else:
                    print("Missing server ID")
            elif splitCommand[0] == "crash":
                crash()
            elif splitCommand[0] == "exit":
                temp = 'exit'
                print("Program terminated")
                os._exit(1)
                
            else:
                print("Command not found")


#Main Program
# It will check for input then it will begin the treads
if arguments_size > 5 : 
    if arguments[1] == "server":
        topologyPath = arguments[3]
        routingUpdateInter = arguments[5]
        readFile(topologyPath)
        global serverThread
        serverThread = threading.Thread(target=server)
        serverThread.demon = True
        serverThread.start()
        menuThread = threading.Thread(target=mainMenu)
        menuThread.demon = True
        menuThread.start()
    else:
        serverError()
else:
    serverError()






