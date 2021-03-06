import csvparser
import preproc
from chinesepostman import eularian, network
import json

def solver(degree = 0, weight = None, start = None):
    edges = None
    edges = csvparser.parse('graph/graph.csv')
    oriedges = edges
    oriedges4json = [{'data':{'source':str(edge[0]),'target':str(edge[1]),'weight':str(edge[2])}} \
        for edge in edges]
    nodes = set(sum([[edge[0],edge[1]] for edge in edges],[]))
    nodes4json = [{'data':{'id':str(n)}} for n in nodes]
    edges = preproc.check_degree(edges, degree)
    edges = preproc.check_weight(edges, weight)
    deledges = [edge for edge in oriedges if edge not in edges]
    if not edges:
        return ['There is no subgraph that meets the specification.', \
            json.dumps(nodes4json).replace('"data"','data').replace('"id"','id'), \
            json.dumps(oriedges4json).replace('"data"','data').replace('"source"','source')\
            .replace('"target"','target').replace('"weight"','weight'),
            [],[],json.dumps(deledges)]
    convert, skip = preproc.check_index(edges)
    nodeinpath = convert
    original_graph = network.Graph(edges)
    if not preproc.check_connected(original_graph):
        return ['The graph is not connected (after meeting the specification).',  \
            json.dumps(nodes4json).replace('"data"','data').replace('"id"','id'), \
            json.dumps(oriedges4json).replace('"data"','data').replace('"source"','source')\
            .replace('"target"','target').replace('"weight"','weight'),
            [],json.dumps(nodeinpath),json.dumps(deledges)]

    #print('{} edges'.format(len(original_graph)))
    if not original_graph.is_eularian:
        #print('Converting to Eularian path...')
        graph = eularian.make_eularian(original_graph)
        #print('Conversion complete')
        #print('\tAdded {} edges'.format(len(graph) - len(original_graph)))
        #print('\tTotal cost is {}'.format(graph.total_cost))
    else:
        graph = original_graph

    if start != None and skip:
        if start not in convert:
            return ['The start node specified does not meet other requirements.', \
            json.dumps(nodes4json).replace('"data"','data').replace('"id"','id'), \
            json.dumps(oriedges4json).replace('"data"','data').replace('"source"','source')\
            .replace('"target"','target').replace('"weight"','weight'),
            [],json.dumps(nodeinpath),json.dumps(deledges)]
        start = convert.index(start) + 1
    #print('Attempting to solve Eularian Circuit...')
    route, attempts = eularian.eularian_path(graph, start=start)
    if not route:
        #print('\tGave up after {} attempts.'.format(attempts))
        return ['Failed to find a route after '+ str(attempts) + ' attempts.', \
            json.dumps(nodes4json).replace('"data"','data').replace('"id"','id'), \
            json.dumps(oriedges4json).replace('"data"','data').replace('"source"','source')\
            .replace('"target"','target').replace('"weight"','weight'),
            [],json.dumps(nodeinpath),json.dumps(deledges)]
    else:
        #print('\tSolved in {} attempts'.format(attempts, route))
        #print('Solution: ({} edges)'.format(len(route) - 1))
        #print('\t{}'.format(route))
        #nodes4json = [{'data':{'id':str(n)}} for n in convert]
        if skip:
            for i, node in enumerate(route):
                route[i] = convert[node-1]
        path4json = [(route[i], route[i+1]) for i in range(len(route)-1)]
        #edges4json = [(edge[0], edge[1]) for edge in edges]
        #oriedges4json.append({'data':{'source':4,'target':1,'weight':2}, 'classes':'diredge'})
        return ['Find path '+'->'.join(map(str,route)), \
            json.dumps(nodes4json).replace('"data"','data').replace('"id"','id'), \
            json.dumps(oriedges4json).replace('"data"','data').replace('"source"','source')\
            .replace('"target"','target').replace('"weight"','weight'),
            json.dumps(path4json),json.dumps(nodeinpath),json.dumps(deledges)]
