import networkx as nx
import matplotlib.pyplot as plt

# networkx 1.11 has a bug with importing the graphviz stuff
from networkx.drawing.nx_agraph import graphviz_layout

class ZObject:
    def __init__(self):
        self.object_id = 0
        self.description = ""
        self.parent_id = 0
        self.child_id = 0
        self.sibling_id = 0

    def object_key(self):
        return str(self.object_id) + "\n" + str(self.description)

    def display_node(self):
        print("Object ID: " + str(self.object_id) + "\nParent ID: " + str(self.parent_id) + "\nChild ID: " +
              str(self.child_id) + "\nSibling ID: " + str(self.sibling_id) + "\nDescription: " + self.description)


class ZGame:
    def __init__(self, object_file):
        self.object_list = []
        self.object_file = object_file

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

            cur_object = ZObject()

            # Parse objects
            for line in file:
                if line.find(". Attributes") != -1:
                    cur_object.object_id = int(line[: line.find(". Attributes")].strip())
                if line.find("Parent object:") != -1:
                    cur_object.parent_id = int(line[line.find("Parent object:") + 14: line.find("Sibling object:")].strip())
                    cur_object.sibling_id = int(line[line.find("Sibling object:") + 15: line.find("Child object:")].strip())
                    cur_object.child_id = int(line[line.find("Child object:") + 13:])
                if line.find("Description:") != -1:
                    cur_object.description = line[line.find("Description:") + 13:].strip()
                    self.object_list.append(cur_object)
                    cur_object = ZObject()

        return title, object_total, len(self.object_list)

    def graph_object_file(self, nodes_to_ignore):
        if len(self.object_list) == 0:
            return

        G = nx.DiGraph()

        for o in self.object_list:
            if o.parent_id in nodes_to_ignore:
                nodes_to_ignore.append(o.object_id)
                continue
            elif o.object_id in nodes_to_ignore:
                continue

            G.add_node(o.object_key())

        for o in self.object_list:
            if o.parent_id != 0 and o.object_id not in nodes_to_ignore:
                G.add_edge(o.object_key(), self.object_list[o.parent_id - 1].object_key())

            if o.sibling_id != 0 and o.object_id not in nodes_to_ignore:
                G.add_edge(o.object_key(), self.object_list[o.sibling_id - 1].object_key())

        pos = graphviz_layout(G, prog='dot')
        nx.draw_networkx(G, pos, node_size=1600, node_color='blue', node_alpha=0.3, node_text_size=12)

        plt.show()
