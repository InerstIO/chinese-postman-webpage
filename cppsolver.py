import csvparser
import preproc
from chinesepostman import eularian, network

def solver(degree = 0, weight = None, start = 1):
    """ Make it so. """
    edges = None
    edges = csvparser.parse('graph/graph.csv')
    edges = preproc.check_degree(edges, degree)
    edges = preproc.check_weight(edges, weight)
    if not edges:
        return 'There is no subgraph that meets the specification.'
    convert = preproc.check_index(edges)
    original_graph = network.Graph(edges)
    if not preproc.check_connected(original_graph):
        return 'The graph is not connected (after meeting the specification).'

    #print('{} edges'.format(len(original_graph)))
    if not original_graph.is_eularian:
        #print('Converting to Eularian path...')
        graph = eularian.make_eularian(original_graph)
        #print('Conversion complete')
        #print('\tAdded {} edges'.format(len(graph) - len(original_graph)))
        #print('\tTotal cost is {}'.format(graph.total_cost))
    else:
        graph = original_graph

    if convert:
        start = convert.index(start) + 1
    #print('Attempting to solve Eularian Circuit...')
    route, attempts = eularian.eularian_path(graph, start = start)
    if not route:
        #print('\tGave up after {} attempts.'.format(attempts))
        return 'Failed to find a route after '+ str(attempts) + ' attempts.'
    else:
        #print('\tSolved in {} attempts'.format(attempts, route))
        #print('Solution: ({} edges)'.format(len(route) - 1))
        #print('\t{}'.format(route))
        if convert:
            for i,node in enumerate(route):
                route[i] = convert[node-1]
        return 'Find path '+'->'.join(map(str,route))