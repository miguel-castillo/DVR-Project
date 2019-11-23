import argparse
import sys
import threading

arguments_size = len(sys.argv)

#funtion to start the server
def server():
    print("Server thread")

#update function
def update():
    print("Update option")

#step function
def step():
    print("Step option")

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
        command = input("Waiting for command: ")
        splitCommand = command.split()
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
            else:
                print("Command not found")


#Main Program
# It will check for input then it will begin the treads
if arguments_size < 6 : # flip sign when sone testing
    print("Reading topology file...")
    serverThread = threading.Thread(target=server)
    serverThread.start()
    menuThread = threading.Thread(target=mainMenu)
    menuThread.start()
    
else:
    print("missing arguments to start the program")
    print("Use the following template:")
    print("server -t  <topology-file-name> -i <routing-update-interval>")
    print("Program terminated")






