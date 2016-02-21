#!/usr/bin/python

import ZObjects as zo

import sys, getopt

import networkx as nx
import matplotlib.pyplot as plt

# networkx 1.11 has a bug with importing the graphviz stuff
from networkx.drawing.nx_agraph import graphviz_layout

def main(argv):
    object_file = ""
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

    if not object_file:
        print('ZTree.py -o <zfile> -n <node1,node2,node3>')
        sys.exit(2)

    z_game = zo.ZGame(object_file)

    title, object_total, object_list_count = z_game.parse_object_file()

    print(title + " " + object_total + " " + str(object_list_count))
    print("Nodes ignored: " + ", ".join(str(i) for i in nodes_to_ignore))

    # Set up graph
    G = nx.DiGraph()

    for o in z_game.object_list:
        if o.parent_id in nodes_to_ignore:
            nodes_to_ignore.append(o.object_id)
            continue
        elif o.object_id in nodes_to_ignore:
            continue
        G.add_node(str(o.object_id) + "\n" + str(o.description))

    for o in z_game.object_list:
        if o.parent_id != 0 and o.object_id not in nodes_to_ignore:
            # flip this around so arrows are right
            G.add_edge(str(z_game.object_list[o.parent_id - 1].object_id) + "\n" + str(z_game.object_list[o.parent_id - 1].description),
                       str(o.object_id) + "\n" + str(o.description))

    pos = graphviz_layout(G, prog='dot')
    nx.draw_networkx(G, pos, node_size=1600, node_color='blue', node_alpha=0.3, node_text_size=12)

    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
