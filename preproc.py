import csvparser
from chinesepostman import network

def check_index(edges):
    '''
    Make the index of the nodes starts from zero, and no skipping.
    Return the list used for conversion (all the existing nodes in order),
    need to use that list to convert everything back after finding the path.
    '''
    if not edges:
        return
    max_index, skip = 1, False
    s = set()
    for edge in edges:
        s.add(edge[0])
        s.add(edge[1])
        max_index = max(max_index, edge[0], edge[1])
    l = list(s)
    if len(s) != max_index:
        skip = True
        for edge in edges:
            edge[0] = l.index(edge[0]) + 1
            edge[1] = l.index(edge[1]) + 1
    return l, skip

def check_degree(edges, deg):
    '''
    Delete the edges which includes nodes with degree lower than deg in the original
    graph.
    Return the new edges
    '''
    graph = network.Graph(edges)
    node2del = [node for node in graph.node_orders if graph.node_orders[node] < deg]
    new_edges = []
    for edge in edges:
        if edge[0] in node2del or edge[1] in node2del:
            continue
        new_edges.append(edge)
    return new_edges

def check_weight(edges, w):
    '''
    Delete edges with weight larger than w.
    Return the new edges
    '''
    if w == None:
        return edges
    new_edges = []
    for edge in edges:
        if edge[2] <= w:
            new_edges.append(edge)
    return new_edges

def check_connected(graph):
    '''
    Check whether the graph is connected.
    '''
    start = graph.edges[0].head
    stack = [start]
    visited = set()  # Visited nodes
    while True:
        if start not in stack:
            stack.append(start)
        visited.add(start)
        nodes = [x for x in graph.node_options(start) \
                    if x not in visited]
        if nodes:
            start = nodes[0]  # Ascending
        else:  # Dead end
            try:
                stack.pop()
                start = stack[-1]  # Go back to the previous node
            except IndexError:  # We are back to the beginning
                break
    return len(visited) == len(graph.nodes)
