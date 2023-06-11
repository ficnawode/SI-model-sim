from __future__ import annotations
import numpy as np
import random

class Node:
    def __init__(self, id: int, infected: bool = False):
        self.id = id
        self.infected = infected
        self.neighbors = []

    def add_neighbor(self, neighbor: Node):
        self.neighbors.append(neighbor)

class Graph:
    def __init__(self, size: int):
        self.size = size
        self.nodes = [Node(i, False) for i in range(self.size)]
        self.number_of_edges = 0

    def tick(self):
        pass

    def create_edge(self, node_id1, node_id2):
        assert(node_id1 < self.size and node_id2 < self.size)
        if node_id1 == node_id2:
            return
        if not node_id1 in self.nodes[node_id2].neighbors:
            self.nodes[node_id1].add_neighbor(self.nodes[node_id2])
            self.nodes[node_id2].add_neighbor(self.nodes[node_id1])
            self.number_of_edges += 1
    
class SIModel(Graph):
    def __init__(self, size, infection_prob):
        super().__init__(size)
        self.infection_prob = infection_prob
        self.amount_of_infected = 0

    def infect_node(self, node_id : int):
        self.amount_of_infected += 1
        self.nodes[node_id].infected = True
    
    def try_infecting_neighbors(self, node)->None:
        if not node.infected:
            return
        for neighbor in node.neighbors:
            should_be_infected = np.random.random() < self.infection_prob
            if (not neighbor.infected) and should_be_infected:
                self.infect_node(neighbor.id)
    
    def tick(self)->None:
        node_indices = list(range(len(self.nodes)))
        random.shuffle(node_indices)
        randomized_nodes = [self.nodes[r] for r in node_indices]
        for node in randomized_nodes:
            self.try_infecting_neighbors(node)

    @staticmethod
    def create_from_correlation_matrix(corr_mat: np.matrix, infection_prob: float)->SIModel:
        g = SIModel(int(np.sqrt(corr_mat.size)), infection_prob)
        for i in range(g.size):
            for j in range(i,g.size):
                should_be_connected = np.random.random() < corr_mat[i,j]
                if should_be_connected:
                    g.create_edge(i,j)
        return g

