class ZObject:
    def __init__(self):
        self.object_id = 0
        self.description = ""
        self.parent_id = 0
        self.child_id = 0

    def display_node(self):
        print("Object ID: " + str(self.object_id) + "\nParent ID: " + str(self.parent_id) + "\nChild ID: " +
              str(self.child_id) + "\nDescription: " + self.description)


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
                    cur_object.child_id = int(line[line.find("Child object:") + 13:])
                if line.find("Description:") != -1:
                    cur_object.description = line[line.find("Description:") + 13:].strip()
                    self.object_list.append(cur_object)
                    cur_object = ZObject()

        return title, object_total, len(self.object_list)
