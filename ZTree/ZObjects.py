class ZObject:
    def __init__(self):
        self.ObjectID = 0
        self.Description = ""
        self.ParentID = 0
        self.ChildID = 0

    def display_node(self):
        print("Object ID: " + str(self.ObjectID) + "\nParent ID: " + str(self.ParentID) + "\nChild ID: " + str(self.ChildID) + "\nDescription: " + self.Description)


class ZGame:
    def __init__(self):
        self.ObjectList = []
