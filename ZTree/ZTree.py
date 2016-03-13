#!/usr/bin/python

import ZObjects as zo
import sys
import getopt


def main(argv):
    version = "0.1"
    help_message = "usage: ZTree.py -o <object_file> -n <node1,node2,node3>" + "\n\n" + "ZTree version " + version + \
                   " - " + "maps Infocom story files into a directional graph. By Nathan Tucker." + "\n\n" + \
                   "\t-o, --objects\tpath to object file (from infodump -o)" + "\n" + \
                   "\t-s, --siblings\tdisplay sibling relations (default false)" + "\n" + \
                   "\t-n, --nodes\tcomma-separated list of nodes to ignore" + "\n" + \
                   "\t-d, --display\tdisplay all nodes(0), only rooms(1), only objects(2), objects in rooms(3)" + "\n\n" + \
                   "example: ZTree.py -o ../Dumps/awaken.z5 -n 1,4,6,118,125\n"

    object_file = ""
    nodes_to_ignore = []
    display_sibling_paths = False
    display_mode = 0

    try:
        opts, args = getopt.getopt(argv, "ho:n:sd:", ["objects=", "nodes=", "siblings", "display="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help_message)
            sys.exit()
        elif opt in ("-o", "--objects"):
            object_file = arg
        elif opt in ("-n", "--nodes"):
            nodes_to_ignore = [int(n.strip()) for n in arg.split(',')]
        elif opt in ("-s", "--siblings"):
            display_sibling_paths = True
        elif opt in ("-d", "--display"):
            display_mode = int(arg)

    if not object_file:
        print(help_message)
        sys.exit(2)

    z_game = zo.ZGame(object_file)

    print("Parsing object file...")

    # Parse the object file
    title, object_total, object_list_count = z_game.parse_object_file()

    print(title + " " + object_total.strip() + "\nNodes Parsed: " + str(object_list_count))
    print("Nodes ignored: " + ", ".join(str(i) for i in nodes_to_ignore))

    # Setup and draw the graph
    if display_mode is 3:
        z_game.graph_traditional_object_file(nodes_to_ignore)
    else:
        z_game.graph_network_object_file(nodes_to_ignore, display_sibling_paths, display_mode)

if __name__ == "__main__":
    main(sys.argv[1:])
