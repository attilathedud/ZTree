import networkx as nx
import matplotlib.pyplot as plt

# networkx 1.11 has a bug with importing the graphviz stuff
from networkx.drawing.nx_agraph import graphviz_layout

ITEM_OBJECT_KEY = 1
ROOM_OBJECT_KEY = 2

class ZObject:
    def __init__(self):
        self.object_id = 0
        self.description = ""
        self.parent_id = 0
        self.child_id = 0
        self.sibling_id = 0
        self.directions = {}
        self.object_type = 0

    def object_key(self):
        return str(self.object_id) + "\n" + str(self.description)

    def display_node(self):
        print("Object ID: " + str(self.object_id) + "\nParent ID: " + str(self.parent_id) + "\nChild ID: " +
              str(self.child_id) + "\nSibling ID: " + str(self.sibling_id) + "\nDescription: " + self.description +
              "\nDirections: " + self.directions)


class ZGame:
    def __init__(self, object_file):
        self.object_list = []
        self.object_file = object_file
        self.compass_id = 0
        self.compass_directions = {}

    def parse_object_file(self):
        with open(self.object_file, 'r') as file:
            # Parse header
            file.readline()
            line = file.readline()
            title = line[line.find("is") + 3:]
            file.readline()
            file.readline()
            file.readline()
            object_total = file.readline()

            is_reading_properties = False
            cur_object = ZObject()

            # Parse objects
            for line in file:
                if is_reading_properties:
                    if line.isspace():
                        is_reading_properties = False

                        self.object_list.append(cur_object)
                        cur_object = ZObject()
                    else:
                        if line.find("[") != -1 and line.find("]") != -1:
                            property_id = int(line[line.find("[") + 1: line.find("]")].strip())
                            property_value = int(line[line.find("]") + 1:].replace(" ", ""), 16)

                            if property_value is not 0 and cur_object.object_id not in self.compass_directions and \
                                    property_id in self.compass_directions.keys():
                                cur_object.directions[self.compass_directions[property_id]] = property_value
                            elif property_id is ITEM_OBJECT_KEY or property_id is ROOM_OBJECT_KEY:
                                cur_object.object_type = property_id
                else:
                    if line.find(". Attributes") != -1:
                        cur_object.object_id = int(line[: line.find(". Attributes")].strip())
                    elif line.find("Parent object:") != -1:
                        cur_object.parent_id = int(line[line.find("Parent object:") + 14: line.find("Sibling object:")].strip())
                        cur_object.sibling_id = int(line[line.find("Sibling object:") + 15: line.find("Child object:")].strip())
                        cur_object.child_id = int(line[line.find("Child object:") + 13:])
                    elif line.find("Description:") != -1:
                        cur_object.description = line[line.find("Description:") + 13:].strip()

                        # Set our game's compass id so we can get future directions
                        if cur_object.description == "\"compass\"":
                            self.compass_id = cur_object.object_id

                        # Add any children of the compass to the compass dict
                        if self.compass_id is not 0 and cur_object.parent_id is self.compass_id:
                            self.compass_directions[cur_object.object_id] = cur_object.description
                    elif line.find("Properties:") != -1:
                        is_reading_properties = True

            self.object_list.append(cur_object)

        return title, object_total, len(self.object_list)

    def graph_object_file(self, nodes_to_ignore):
        if len(self.object_list) == 0:
            return

        G = nx.DiGraph()

        node_items_list = []
        node_rooms_list = []
        node_unknowns_list = []

        for o in self.object_list:
            if o.parent_id in nodes_to_ignore:
                nodes_to_ignore.append(o.object_id)
                continue
            elif o.object_id in nodes_to_ignore:
                continue

            G.add_node(o.object_key())

            if o.object_type is ITEM_OBJECT_KEY:
                node_items_list.append(o.object_key())
            elif o.object_type is ROOM_OBJECT_KEY:
                node_rooms_list.append(o.object_key())
            else:
                node_unknowns_list.append(o.object_key())

        for o in self.object_list:
            if o.parent_id != 0 and o.object_id not in nodes_to_ignore:
                G.add_edge(self.object_list[o.parent_id - 1].object_key(), o.object_key(), direction="")

            if o.sibling_id != 0 and o.object_id not in nodes_to_ignore:
                G.add_edge(self.object_list[o.sibling_id - 1].object_key(), o.object_key(), direction="")

            for direction, node in o.directions.items():
                if node < len(self.object_list):
                    G.add_edge(o.object_key(), self.object_list[node-1].object_key(), direction=direction)

        pos = graphviz_layout(G, prog='dot')
        nx.draw_networkx(G, pos,
                         node_size=500,
                         alpha=0.6, font_size=8)

        edge_labels = dict([((u, v,), d['direction'])
                            for u, v, d in G.edges(data=True)])

        nx.draw_networkx_nodes(G, pos, nodelist=node_items_list,
                               node_color="r", node_size=500, alpha=0.6)
        nx.draw_networkx_nodes(G, pos, nodelist=node_rooms_list,
                               node_color="b", node_size=500, alpha=0.6)
        nx.draw_networkx_nodes(G, pos, nodelist=node_unknowns_list,
                               node_color="y", node_size=500, alpha=0.6)

        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos, font_size=8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, alpha=0.6)

        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        plt.show()
