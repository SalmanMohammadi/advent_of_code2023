from __future__ import annotations
from typing import List, Tuple, Union
from dataclasses import dataclass
from typing import Optional
import time
import math

@dataclass
class Node:
    value: str
    left: Optional[Node] = None
    right: Optional[Node] = None

    def __eq__(self, node: Union[Node, str]) -> bool:
        if isinstance(node, str):
            return self.value == node
        return hasattr(node, "value") and self.value == node.value
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __repr__(self) -> str:
        return f"\nNode {self.value}: [left: {self.left.value}, right: {self.right.value}]" 

    def traverse(self, instruction: str) -> Node:
        assert instruction in ["R", "L"]
        if instruction == "R":
            return self.right
        return self.left

class Map:
    def __init__(self, node_values: List[str], leaf_values: List[Tuple[str, str]]):
        self.starting_nodes = []
        self.nodes = dict()
        for (node_value, (left_value, right_value)) in zip(node_values, leaf_values):
            node = Node(node_value)
            if node_value in self.nodes:
                node = self.nodes[node_value]
            if left_value in self.nodes:
                node.left = self.nodes[left_value]
            else:
                node.left = Node(left_value)
                self.nodes[left_value] = node.left
            if right_value in self.nodes:
                node.right = self.nodes[right_value]
            else:
                node.right = Node(right_value)
                self.nodes[right_value] = node.right
            self.nodes[node_value] = node
            if node_value.endswith("A"):
                self.starting_nodes.append(node_value)

    def traverse_instructions(self, node: Node, instructions: str) -> Node:
        for instruction in instructions:
            node = node.traverse(instruction)
        return node
    
    def find_shortest_path(self, instructions: str) -> int:
        i = 0
        node = self.nodes["AAA"]
        while node != "ZZZ":
            node = self.traverse_instructions(node, instructions)
            i += len(instructions)
        return i
    
    def find_shortest_simultaneous_path(self, instructions: str) -> int:
        i = 0
        nodes = [self.nodes[node_value] for node_value in self.starting_nodes]
        steps_to_z = [0 for _ in nodes]
        while not all([step > 0 for step in steps_to_z]):
            for instruction in instructions:
                nodes = [node.traverse(instruction) for node in nodes]
            i += len(instructions)
            for j, node in enumerate(nodes):
                if steps_to_z[j] == 0 and "Z" in node.value:
                    steps_to_z[j] = i
        return math.lcm(*steps_to_z)

    def __repr__(self) -> str:
        return str.join("", [str(x) for x in self.nodes])
    

if __name__ == "__main__":
    with open("input") as f:
        inpt = f.read().split('\n')
        instructions = inpt[0]
        nodes, leaf_values = zip(*[x.split(" = ") for x in inpt[2:]])
        leaf_values = [tuple(x.replace("(", "").replace(")", "").split(", ")) for x in leaf_values]
        m = Map(nodes, leaf_values)

        start = time.time()
        result = m.find_shortest_path(instructions)
        end = time.time()
        print(f"Part one: {result} taking {(end - start):.4f}s")

        start = time.time()
        result = m.find_shortest_simultaneous_path(instructions)
        end = time.time()
        print(f"Part two: {result} taking {(end - start):.4f}s")