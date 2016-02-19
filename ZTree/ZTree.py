#!/usr/bin/python

import ZObjects as zo

import sys, getopt

import networkx as nx
import matplotlib.pyplot as plt

# networkx 1.11 has a bug with importing the graphviz stuff
from networkx.drawing.nx_agraph import graphviz_layout

def main(argv):
    object_file = ''
    nodes_to_ignore = []

    try:
        opts, args = getopt.getopt( argv, "ho:n:", ["objects=", "nodes="])
    except getopt.GetoptError:
        print('ZTree.py -o <zfile> -n <node1,node2,node3>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('ZTree.py -o <zfile> -n <node1,node2,node3>')
            sys.exit()
        elif opt in ("-o", "--objects"):
            object_file = arg
        elif opt in ("-n", "--nodes"):
            nodes_to_ignore = [int(n.strip()) for n in arg.split(',')]

    z_game = zo.ZGame()

    with open('../Dumps/awaken.z5_object_dump', 'r') as file:

        # Parse header
        file.readline()
        line = file.readline()
        title = line[line.find("is") + 3:]
        file.readline()
        file.readline()
        file.readline()
        objectTotal = file.readline()

        curObject = zo.ZObject()

        # Parse objects
        for line in file:
            if line.find(". Attributes") != -1:
                curObject.ObjectID = int(line[: line.find(". Attributes")].strip())
            if line.find("Parent object:") != -1:
                curObject.ParentID = int(line[line.find("Parent object:") + 14: line.find("Sibling object:")].strip())
                curObject.ChildID = int(line[line.find("Child object:") + 13:])
            if line.find("Description:") != -1:
                curObject.Description = line[line.find("Description:") + 13:].strip()
                z_game.ObjectList.append(curObject)
                curObject = zo.ZObject()

    print(title + " " + objectTotal)
    print("Nodes ignored: " + ", ".join(str(i) for i in nodes_to_ignore))

    # Set up graph
    G = nx.DiGraph()

    for o in z_game.ObjectList:
        if o.ParentID in nodes_to_ignore:
            nodes_to_ignore.append(o.ObjectID)
            continue
        elif o.ObjectID in nodes_to_ignore:
            continue
        G.add_node(str(o.ObjectID) + "\n" + str(o.Description))

    for o in z_game.ObjectList:
        if o.ParentID != 0 and o.ObjectID not in nodes_to_ignore:
            # flip this around so arrows are right
            G.add_edge(str(z_game.ObjectList[o.ParentID - 1].ObjectID) + "\n" + str(z_game.ObjectList[o.ParentID - 1].Description),
                       str(o.ObjectID) + "\n" + str(o.Description))

    pos = graphviz_layout(G, prog='dot')
    nx.draw_networkx(G, pos, node_size=1600, node_color='blue', node_alpha=0.3, node_text_size=12)

    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])