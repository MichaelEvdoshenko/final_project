class Tree():
    def __init__(self, count_win = 0, count_inbound = 0, value = [-1, -1], UBC1 = 10.0):
        self.value = value
        self.parent = None 
        self.count_win = count_win
        self.count_inbound = count_inbound
        self.UBC1 = UBC1
        self.children = []

    def add_child(self, child_node):
        child_node.parent = self
        self.children.append(child_node)
