import heapq
import re
import matplotlib.pyplot as plt
import timeit
from collections import deque, defaultdict
import sys


class Node:

    def __init__(self, name):
        self.name = name
        self.edge_list = []

    def connect(self, node):
        con = (self.name, node.name)
        self.edge_list.append(con)


class Edge:

    def __init__(self, left, right, weight):
        self.left = left
        self.right = right
        self.weight = weight


class Graph:

    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_node(self, node):
        self.vertices[node.name] = node

    def add_edge(self, left, right, weight):
        if left.name not in self.vertices:
            self.vertices[left.name] = left

        if right.name not in self.vertices:
            self.vertices[right.name] = right

        edge = Edge(left, right, weight)

        key = (left.name, right.name)
        self.edges[key] = edge

        key = (right.name, left.name)
        self.edges[key] = edge

        left.connect(right)
        right.connect(left)

    def breadth_first_search(self, graph, source, destination):
        queue = deque()
        visited = {source: 1}
        parent = {}
        queue.append(source)
        while queue:
            last = queue.popleft()
            if last == destination:
                node = last
                path = []
                while node:
                    path.append(node)
                    node = parent.get(node, None)
                return path[::-1]
            for neighbors in graph[last]:
                if neighbors[0] not in visited:
                    visited[neighbors[0]] = 1
                    parent[neighbors[0]] = last
                    queue.append(neighbors[0])
        return "path not found"

    def deepth_first_search(self, graph, source, destination):
        stack = []
        visited = {source: 1}
        path = []
        stack.append(source)
        while stack:
            last = stack.pop()
            path.append(last)
            if last == destination:
                return path
            else:
                for neighbor in graph[last]:
                    if neighbor[0] not in visited:
                        visited[neighbor[0]] = 1
                        stack.append(neighbor[0])
        return "not found"

    def dijkstras(self, graph, source, destination):
        nodes_distance = defaultdict(lambda: float('inf'))
        visited = set()
        nodes_distance[source] = 0
        heap = []
        heapq.heappush(heap, (0, source))
        parent = {}
        path = [source]
        parent[source] = None
        while len(heap) != 0:
            (shortest_distance, current_node) = heapq.heappop(heap)
            if current_node == destination:
                node = current_node
                path = []
                while node:
                    path.append(node)
                    node = parent.get(node, None)
                return path[::-1]
            for neighbor in graph[current_node]:
                if neighbor[0] not in visited:
                    prev_distance = nodes_distance[neighbor[0]]
                    curr_distance = nodes_distance[current_node] + neighbor[1]
                    if curr_distance < prev_distance:
                        heapq.heappush(heap, (curr_distance, neighbor[0]))
                        nodes_distance[neighbor[0]] = curr_distance
                        parent[neighbor[0]] = current_node
        return "not found"

    def heuristic_fun(self, h_nodes, node):
        return h_nodes[node]

    def astrix_search(self, graph, h_nodes, source, destination):
        visited_uninspected = {source}
        visited_inspected = set([])
        distance = {source: 0}
        parents = {source: source}
        while len(visited_uninspected) > 0:
            node = None
            for node_visited in visited_uninspected:
                if node is None or distance[node_visited] + self.heuristic_fun(h_nodes, node_visited) < distance[node] + self.heuristic_fun(h_nodes, node):
                    node = node_visited
            if node is None:
                return 'Path does not exist!'
            if node == destination:
                paths = []

                while parents[node] != node:
                    paths.append(node)
                    node = parents[node]

                paths.append(source)

                paths.reverse()

                return paths
            for (node_connected, weight) in graph[node]:
                if node_connected not in visited_uninspected and node_connected not in visited_inspected:
                    visited_uninspected.add(node_connected)
                    parents[node_connected] = node
                    distance[node_connected] = distance[node] + weight
                else:
                    if distance[node_connected] > distance[node] + weight:
                        distance[node_connected] = distance[node] + weight
                        parents[node_connected] = node

                        if node_connected in visited_inspected:
                            visited_inspected.remove(node_connected)
                            visited_uninspected.add(node_connected)
            visited_uninspected.remove(node)
            visited_inspected.add(node)
        return 'Path does not exist!'


def create_graph(file):
    inf = sys.maxsize
    graph = Graph()
    adj_list = {}
    nodes = {}
    h_nodes = {}

    with open(file, "r") as ef:
        for edges in ef:
            edges_content = re.split('[:\n]', edges)
            graph.add_edge(Node(edges_content[0]), Node(edges_content[1]), edges_content[2])

    for iv, (k, edge) in enumerate(graph.edges.items()):
        if k[0] not in adj_list:
            adj_list[k[0]] = [(k[1], int(edge.weight))]
        else:
            adj_list[k[0]].append((k[1], int(edge.weight)))
    for key in graph.vertices.keys():
        h_nodes[key] = 1
        nodes[key] = {"distance": inf, "path": []}

    bfs = 0
    time_taken = []
    for key in graph.vertices.keys():
        first_bfs = timeit.default_timer()
        for k in graph.vertices.keys():
            print(graph.breadth_first_search(adj_list, key, k))
        second_bfs = timeit.default_timer()
        bfs += (second_bfs - first_bfs)
    time_taken.append(bfs / 400)

    dfs = 0
    for key in graph.vertices.keys():
        first_dfs = timeit.default_timer()
        for k in graph.vertices.keys():
            print(graph.deepth_first_search(adj_list, key, k))
        second_dfs = timeit.default_timer()
        dfs += (second_dfs - first_dfs)
    time_taken.append(dfs / 400)

    djk = 0
    for key in graph.vertices.keys():
        first_dj = timeit.default_timer()
        for k in graph.vertices.keys():
            print(graph.dijkstras(adj_list, key, k))
        second_dj = timeit.default_timer()
        djk += (second_dj - first_dj)
    time_taken.append(djk / 400)

    astar = 0
    for key in graph.vertices.keys():
        first_as = timeit.default_timer()
        for k in graph.vertices.keys():
            print(graph.astrix_search(adj_list, h_nodes, key, k))
        second_as = timeit.default_timer()
        astar += (second_as - first_as)
    time_taken.append(astar / 400)

    search_algorithms = ["bfs", "dfs", "dijkstras", "astar"]
    plt.figure(figsize=(9, 5))
    plt.bar(search_algorithms, time_taken)
    plt.suptitle('search algorithm Plotting')
    plt.xlabel("search_algorithms")
    plt.ylabel("Average time taken")
    plt.show()


create_graph("edges.text")
