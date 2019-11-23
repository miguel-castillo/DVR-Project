import argparse

def create_line_array(content):
    array = []
    for line in content.splitlines():
        array.append(line)
    return array

def create_topology(topology_string):
    lines = create_line_array(topology_string)
    for i in range(9):
        print(lines[i])



parser = argparse.ArgumentParser()
parser.add_argument("-t", type=str, required=True)
parser.add_argument("-i", type=int, required=True)

args = parser.parse_args()

t = args.t
topology_file = open(t, "r")
contents = ""
if topology_file.mode == 'r':
    contents = topology_file.read()
topology_file.close()
create_topology(contents)


#class Topology: