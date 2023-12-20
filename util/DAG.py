'''
Need to have

def generate_DAG(Task_table, Delay_matrix)


def random_initial_generation(population_size, DAG)


'''

import numpy as np
import random

class DAG:
    def __init__(self, delay_cost_matrix):
        #assert np.shape(delay_cost_matrix) == (5, 5), "Delay cost matrix must be a 5x5 numpy array"
        self.graph = {}
        self.node_weights = {}
        self.setup_costs = {}  # 存儲設置成本
        self.delay_cost_matrix = delay_cost_matrix

    def add_setup_edge_cost(self, from_node, to_node, setup_cost):
        self.setup_costs[(from_node, to_node)] = setup_cost

        if from_node not in self.graph:
            self.graph[from_node] = []
        self.graph[from_node].append(to_node)

        if to_node not in self.graph:
            self.graph[to_node] = []

    def add_node_task_cost(self, node, task_cost):
        self.node_weights[node] = task_cost

    def display(self):
        for node in self.graph:
            formatted_node = f"{node:02}"
            formatted_edges = ' '.join(f"{end_node:02}" for end_node in self.graph[node])
            print(f"{formatted_node} -> {formatted_edges}")

        print("\nNode Task Costs:")
        for node, weight in self.node_weights.items():
            print(f"{node:02}: {weight}")

        print("\nSetup Edge Costs:")
        for edge, cost in self.setup_costs.items():
            print(f"{edge}: {cost}")
        print("\nDelay Cost Matrix:")
        print(self.delay_cost_matrix)

    def random_topological_sort(self):
        in_degree = {u: 0 for u in self.graph}  # 初始化所有顶点的入度为0
        for u in self.graph:
            for v in self.graph[u]:
                in_degree[v] = 0
                in_degree[v] += 1

        queue = [u for u in in_degree if in_degree[u] == 0]  # 所有入度为0的顶点
        top_order = []

        while queue:
            u = random.choice(queue)
            queue.remove(u)
            top_order.append(u)

            for v in self.graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return top_order
    
    def get_parent_nodes(self, node_id):
        parent_nodes = []
        for parent, children in self.graph.items():
            if node_id in children:
                parent_nodes.append(parent)
        return parent_nodes



