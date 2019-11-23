import argparse
import sys
import threading

arguments_size = len(sys.argv)

#funtion to start the server
def server():
    print("Server thread")
    
# main menu function
def mainMenu():
    print("You can enter a command at any time")
    temp = ''
    while temp != 'exit' :
        command = input("Waiting for command: ")
        if command == 'update':
            print("Update option")
        elif command == "step":
            print("Step option")
        elif command == "packets":
            print("Packets option")
        elif command == "display":
            print("Display option")
        elif command == "disable":
            print("Disable option")
        elif command == "crash":
            print("Crash option")
        elif command == "exit":
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






