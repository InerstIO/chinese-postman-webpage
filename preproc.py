import csvparser
from chinesepostman import network

def check_index(edges):
    '''
    Make the index of the nodes starts from zero, and no skipping.
    Return the list used for conversion, need to use that list to convert 
    everything back after finding the path.
    If no conversion, return an empty list.
    '''
    if not edges:
        return
    max_index = 1
    s = set()
    for edge in edges:
        s.add(edge[0])
        s.add(edge[1])
        max_index = max(max_index, edge[0], edge[1])
    if len(s) != max_index:
        l = list(s)
        for edge in edges:
            edge[0] = l.index(edge[0]) + 1
            edge[1] = l.index(edge[1]) + 1
        return l
    return []
    #####   BAD NEED TO REGENERATE GRAPH, BETTER TO DO WITH EDGES
    '''
    if not graph.all_edges:
        return
    maxIndex=1
    s=set()
    for edge in graph.all_edges:
        s.add(edge.head)
        s.add(edge.tail)
        maxIndex=max(maxIndex, edge.head, edge.tail)
    if len(s) != maxIndex:
        l=list(s)
        for edge in graph.all_edges:
            edge.head=l.index(edge.head)+1
            edge.tail=l.index(edge.tail)+1
    '''

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

