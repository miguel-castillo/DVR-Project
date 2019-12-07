Distance Vector Protocol

In this assignment you will implement a simplified version of the Distance Vector Routing Protocol.
The protocol will be run on top of four servers/laptops (behaving as routers) using TCP or UDP. Each
server runs on a machine at a pre-defined port number. The servers should be able to output their
forwarding tables along with the cost and should be robust to link changes. A server should send out
routing packets only in the following two conditions: a) periodic update and b) the user uses
command asking for one. This is a little different from the original algorithm which immediately sends
out update routing information when routing table changes

Members:
	--> Miguel Angel Castillo  CIN: 304751946
	--> Misael Corvera CIN: 306012790
	--> Judith Cabrera CIN: 304306501
	--> Hummam Sagga CIN: 305082406


## Prerequisites:

	Needs to have Python3 on your computer in order to run the program.


## Run the program:

	On the command line, make sure you are in the same directory as the project. Go to the src folder. Run "Python3 menu.py server -t  <topology-file-name> -i <routing-update-interval>"

