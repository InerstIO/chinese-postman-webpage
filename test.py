import csvparser
import preproc
from chinesepostman import eularian, network

edges = csvparser.parse('brokengraph.csv')
graph = network.Graph(edges)
print(edges)
preproc.check_index(edges)
print(edges)