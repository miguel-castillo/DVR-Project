import argparse
import sys, os
import threading
import socket, pickle
import networkx as nx
import time

arguments_size = len(sys.argv)
arguments = sys.argv
global my_port
global my_server_port
global my_server
global servers
global G
global server_id
global interval
global packetsRe 
global server_block
global crashTemp
global shortest_path

#reading topology file
def readFile(path):
    global servers
    global my_server_port
    global server_id
    global packetsRe
    packetsRe = 0
    servers = []
    edges = []
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    print(HOST)
    print("Reading file...")
    topologyStr = []
    with open(path) as my_file:
        for line in my_file:
            temp = line.split()
            if len(temp) > 2 and  temp[1].find('.') !=-1:
                servers.append(line)
                if temp[1] == HOST:
                    if checkPort(temp[1], temp[2]) == True:
                        my_server_port = int(temp[2]) #Assign port number base on ip address
                        server_id = temp[0]
            elif len(temp) > 2 and  temp[1].find('.') ==-1:
                edges.append(line)
            topologyStr.append(line) 
    #Add nodes and edges from file
    global G
    G = nx.Graph()
    tempNode = []
    nodes = topologyStr[1]
    formated_edges = format_edges(edges)
    G.add_nodes_from(nodes)
    G.add_edges_from(formated_edges)
    # Initialise routing table for every node
    for node in G.nodes:
        if node == '\n':
            tempNode.append(node)
        else:
            G.nodes[node]['routing_table'] = RoutingTable(node)
    #Removes extra empty nodes
    for item in tempNode :
        G.remove_node(item)
    print("File read and Routing Table initialized...")

#Checks to see if port is available
def checkPort(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.bind((ip, int(port)))
        s.close()
        return True
    except:
        return False

# Formats edges according to the graph edge required form: a tuple with a weight i.e. (src, dest, {'weight':5})
def format_edges(raw_edges):
    edges = []
    for edge in raw_edges:
        edges.append((edge[0], edge[2], {'weight': float(edge[4])}))
    return edges

#Error message for invalid server command
def serverError():
    print("Missing arguments to start the program.")
    print("Use the following template:")
    print("server -t  <topology-file-name> -i <routing-update-interval>")
    print("Program terminated")


#funtion to start the server
def server():
    print("Server started at port: ",my_server_port," with update interval = ",interval, " seconds")
    hostname = socket.gethostname()
    HOST = socket.gethostbyname(hostname)
    global my_server
    global packetsRe
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_server:
        my_server.bind((HOST, my_server_port))
        #waiting to receive any message
        while crashTemp == True:
            data, address = my_server.recvfrom(4096)
            data_arr = pickle.loads(data)
            myId = 0
            for t in servers:
                    m = t.split()
                    if m[1] == address[0]:
                        myId = m[0]
            if len(server_block) > 0:
                for s in server_block:
                    if s != address[0]:
                        packetsRe += 1
                        print("Received message from server ", myId)
                        i = 0
                        while i < len(data_arr):
                            if data_arr[i] != data_arr[i+1]:
                                update(data_arr[i], data_arr[i+1], data_arr[i+2]) 
                            i += 3
                    
                        print("Waiting for command: ")
            else:
                packetsRe += 1
                print("Received message from server ", myId)
                i = 0
                while i < len(data_arr):
                    if data_arr[i] != data_arr[i+1]:
                        update(data_arr[i], data_arr[i+1], data_arr[i+2]) 
                    i += 3
                print("Waiting for command: ")
            

#update function
def update(server1, server2, linkCost):
    for node in G.nodes:
        if node == server1 :
            update_routing_table(server1, server2, float(linkCost))

def update_routing_table(src, dest, cost):
    G.nodes[src]['routing_table'].update_edge(dest, cost)
    G.nodes[dest]['routing_table'].update_edge(src, cost)

#Function that will keep sending updates with a set interval
def persistenUpdate():
    while True:
        time.sleep(int(interval))
        for node in G.nodes():
            if node == server_id:
                step(node)
                break
    

#step function
def step(node):
    blockid = []
    for ser in servers:
        tempS = ser.split()
        for s in server_block:
            if tempS[1] == s:
                blockid.append(tempS[0])
                break
        
    message = []
    routing_table = G.nodes[node]['routing_table'].routing_table
    for n in routing_table:
        #Getting rid of extra space
        if n != '\n':
            message.append(node)
            message.append(n)
            message.append(routing_table[n])
    data_string = pickle.dumps(message)
    for s in servers:
        temp = s.split()
        HOST = temp[1]              # The server's hostname or IP address
        PORT = int(temp[2])         # The port used by the server
        skip = False
        if temp[0] != server_id:
            if len(blockid) > 0:
                for bId in blockid:
                    if temp [0] == bId:
                        skip = True
                        break

                if skip != True:
                    my_server.sendto(data_string, (HOST, PORT))
            else:
                my_server.sendto(data_string, (HOST, PORT))
   

#packets function
def packets():
    global packetsRe
    print("Number of packets received = "+ str(packetsRe))
    packetsRe = 0


#display function
def display(node):
    routing_table = G.nodes[node]['routing_table'].routing_table
    print("Routing table for %s:" % node)
    print("Source","\t", "    Destination", "\t", "Cost","\t", "Shortest Cost", "\t", "   Shortest Path" )
    print("-------------------------------------------------------------------------------")
    for n in routing_table:
        #Getting rid of extra space
        if n != '\n':
            if n != server_id:      
                shortest = findPath(node,n)
                print(node,"\t \t", n, "\t \t", routing_table[n],"\t \t",shortest,"\t \t", shortest_path)
            else:
                print(node,"\t \t", n, "\t \t", routing_table[n],"\t \t","0","\t \t", "0")
    print("-------------------------------------------------------------------------------")

#finds all the possible paths from point a to b
def findPath(src,dest):
    global shortest_path
    paths = [p for p in nx.all_simple_paths(G, src, dest)]
    if len(paths) >1:
        temp = []
        for path in paths:
            temp.append(getDistance(path))
        i = 0
        current_short = 0
        while i <len(temp):
            if temp[i] != 0:
                if i < 1:
                    current_short = temp[i]
                    shortest_path = paths[i]
                else:
                    if temp[i] < current_short:
                        current_short = temp[i]
                        shortest_path = paths[i]
            i += 1
        return current_short

#gets the cost from point a to b
def getLength(src, dest):
    length = G.nodes[src]['routing_table'].routing_table[dest]
    return length

#gets the distance from point a to b to c
def getDistance(element):
    i = 0
    distance = 0
    while i < len(element)-1:
        distance += getLength(element[i],element[i+1])
        i += 1
    return distance
    

#disable function
def disable(serverId):
    global server_block
    my_temp_arr = []
    for s in servers:
        temp = s.split()
        id = temp[0] 
        if id == serverId :
            update(server_id,serverId,"inf")
            print("Disable link ",server_id," -> ", id)
            my_temp_arr.append(temp[1])
    for n in G.nodes():
        step(n)
    server_block = my_temp_arr
    print("Done")

#crash function
def crash():
    global my_server
    global crashTemp
    print("Crashing all links...")
    for s in servers: 
        temp = s.split()
        id = temp[0]
        disable(id)
    crashTemp = False
    print("Done!")

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
                    update(splitCommand[1], splitCommand[2], splitCommand[3])
                    print("Update SUCCESS")
                else:
                    print("Missing arguments")
                    print("Use the following template:")
                    print("update <server-ID1> <server-ID2> <Link Cost>")
            elif splitCommand[0] == "step":
                for node in G.nodes:
                    if node == server_id:
                        step(node)
                        print("Step SUCCESS")
                        break
            elif splitCommand[0] == "packets":
                packets()
            elif splitCommand[0] == "display":
                for node in G.nodes:
                    if node == server_id:
                        display(node)
                        break
            elif splitCommand[0] == "disable":
                if len(splitCommand) > 1 :
                    if splitCommand[1].isnumeric() :
                        disable(splitCommand[1])
                    else:
                        print("Enter a number for server ID")
                else:
                    print("Missing server ID")
            elif splitCommand[0] == "crash":
                crash()
                print("server crashed")
                os._exit(1)
            elif splitCommand[0] == "exit":
                temp = 'exit'
                print("Program terminated")
                os._exit(1)
                
            else:
                print("Command not found")

#creates table for a specific node... Also updates table value
class RoutingTable:

    def __init__(self, node):
        global G
        self.name = node
        self.routing_table = {adj_node:G.adj[node][adj_node]['weight'] for adj_node in G.adj[node]} # add adjacent nodes to the routing table
        non_adjacent_nodes = list(set(G.nodes) - set(G.adj[node]) - set(node)) 
        self.routing_table.update({non_adj_node: float('inf') for non_adj_node in non_adjacent_nodes}) # add non-adjacent nodes to the routing table
        self.routing_table[node] = 0
    
    def update_edge(self, dest, cost):
        self.routing_table.update({dest: cost})



#Main Program
# It will check for input then it will begin the treads
if arguments_size > 5 : 
    if arguments[1] == "server":
        topologyPath = arguments[3]
        readFile(topologyPath)
        global serverThread
        global interval 
        global server_block
        global crashTemp
        crashTemp = True
        server_block = []
        interval = int(arguments[5])
        serverThread = threading.Thread(target=server)
        serverThread.demon = True
        serverThread.start()
        menuThread = threading.Thread(target=mainMenu)
        menuThread.demon = True
        menuThread.start()
        # updateThread = threading.Thread(target=persistenUpdate)
        # updateThread.daemon = True
        # updateThread.start()
    else:
        serverError()
else:
    serverError()






