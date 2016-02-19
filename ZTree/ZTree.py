import ZObjects as zo

import networkx as nx
import matplotlib.pyplot as plt

# networkx 1.11 has a bug with importing the graphviz stuff
from networkx.drawing.nx_agraph import graphviz_layout

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

# Set up graph
G = nx.DiGraph()

for o in z_game.ObjectList:
    G.add_node(str(o.ObjectID) + "\n" + str(o.Description))

for o in z_game.ObjectList:
    if o.ParentID != 0:
        G.add_edge(str(z_game.ObjectList[o.ParentID - 1].ObjectID) + "\n" + str(z_game.ObjectList[o.ParentID - 1].Description),
                   str(o.ObjectID) + "\n" + str(o.Description))

pos = graphviz_layout(G, prog='dot')
nx.draw_networkx(G, pos, node_size=1600, node_color='blue', node_alpha=0.3, node_text_size=12)

plt.show()
