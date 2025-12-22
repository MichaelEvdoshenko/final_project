from typing import List, Optional


class Tree:
    def __init__(self,
                 count_win: int = 0,
                 count_inbound: int = 0,
                 value: Optional[List[int]] = None,
                 UBC1: float = 10.0) -> None:
        if value is None:
            value = [-1, -1]
        self.value: List[int] = value
        self.parent: Optional['Tree'] = None
        self.count_win: int = count_win
        self.count_inbound: int = count_inbound
        self.UBC1: float = UBC1
        self.children: List['Tree'] = []

    def add_child(self, child_node: 'Tree') -> None:
        child_node.parent = self
        self.children.append(child_node)
