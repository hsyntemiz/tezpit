import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import time
import matplotlib.pyplot as plt
import time

from collections import defaultdict, deque


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial):
    #visited = {initial: 0}
    visited = {initial: [1000,0,0,0]}
    #visited = [99909,9990,99999990]

    path = {}
    beta=0.8

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node][0] < visited[min_node][0]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]
        print graph.edges
        for edge in graph.edges[min_node]:
            try:
                weight=[]
                #weight = current_weight + graph.distances[(min_node, edge)][0]+ graph.distances[(min_node, edge)][1]
                pathBw=min(current_weight[0],graph.distances[(min_node, edge)][0])
                pathDelay=current_weight[1]+ graph.distances[(min_node, edge)][1]
                hopCount=current_weight[2]+ 1

                fuzzBw=calc_pxy(pathBw,100,1000)
                fuzzHop=calc_hxy(hopCount,1,10)

                #fuzzBw = calc_pxy(pathDelay, 100, 1000)
                fuzzTotal=beta*min(fuzzBw,fuzzHop)+ (1-beta)*1/3*(fuzzBw+fuzzHop)
                weight= [pathBw, pathDelay,hopCount,fuzzTotal ]
                #weight[2]=current_weight[2]+beta*min(graph.distances[(min_node, edge)][0],graph.distances[(min_node, edge)][1])
                #weight=current_weight + beta*min(graph.distances[(min_node, edge)][0],graph.distances[(min_node, edge)][1])+(1-beta)*1/3*(graph.distances[(min_node, edge)][0]+graph.distances[(min_node, edge)][1])
                # weight=beta*min(graph.distances[(min_node, edge)][0],graph.distances[(min_node, edge)][1])+       (1-beta)*1/3*(graph.distances[(min_node, edge)][0],graph.distances[(min_node, edge)][1])

                #######print 'edge:',edge,'- weight',weight,'-- current_weight',current_weight
            except:
                continue
            if edge not in visited or weight[3] > visited[edge][3]:
                visited[edge] = weight
                path[edge] = min_node
                print 'UPDATE for edge:',edge,'- weight',weight,'-- current_weight',current_weight
    print 'visited',visited

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)

def calc_pxy(x,minBw=100,maxBw=1000):

    if x < minBw:

        return 0.25

    if minBw < x <maxBw:


        return 0.75*(x-minBw)/(maxBw-minBw+0.0)+0.25

    if maxBw<x:
        return 1

def calc_hxy(x,minH,maxH):
    m = 0.4
    if x<=minH:
        return 1
    if minH<x<=maxH:
        return ((maxH-x)*(1-m)/(maxH-minH))+m
        #return (x-minH)/(3/4*(maxH-minH))
    if maxH<x:
        return 0

def calc(input1,input2,input3):

    x_hop = np.arange(0, 1000, 1)
    x_delay = np.arange(0, 600, 1)
    x_loss = np.arange(1, 11, 1)

    bandwidth = ctrl.Antecedent(x_hop, 'bandwidth')
    delay = ctrl.Antecedent(x_delay, 'delay')
    lossCount = ctrl.Antecedent(x_loss, 'lossCount')

    tip = ctrl.Consequent(np.arange(0, 11, 1), 'tip')

    names = ['lo', 'md', 'hi']

    #bandwidth.automf(names=names)
    #delay.automf(names=names)
    #tip.automf(names=names)
    # Generate fuzzy membership functions
    bandwidth['lo']= fuzz.trimf(x_hop, [0, 0, 400])  # (start,top,stop)
    bandwidth['md'] = fuzz.trimf(x_hop, [100, 500, 900])
    bandwidth['hi'] = fuzz.trimf(x_hop, [600, 1000, 1000])


    delay['lo']= fuzz.trimf(x_delay, [0, 0, 240])  # (start,top,stop)
    delay['md'] = fuzz.trimf(x_delay, [60, 300, 540])
    delay['hi']  = fuzz.trimf(x_delay, [360, 600, 600])


    lossCount['lo']= fuzz.trimf(x_loss, [0, 0, 4])  # (start,top,stop)
    lossCount['md'] = fuzz.trimf(x_loss, [1, 5, 9])
    lossCount['hi'] = fuzz.trimf(x_loss, [6, 10, 10])

    tip['lo'] = fuzz.trimf(tip.universe, [0, 0, 5])
    tip['md'] = fuzz.trimf(tip.universe, [0, 5, 11])
    tip['hi']  = fuzz.trimf(tip.universe, [5, 11, 11])


    rule1 = ctrl.Rule(antecedent=(
        (bandwidth['lo'] & delay['lo'] & lossCount['lo']) |
        (bandwidth['lo'] & delay['lo'] & lossCount['md']) |
        (bandwidth['lo'] & delay['lo'] & lossCount['hi']) |
        (bandwidth['lo'] & delay['md'] & lossCount['lo']) |
        (bandwidth['lo'] & delay['md'] & lossCount['md']) |
        (bandwidth['lo'] & delay['md'] & lossCount['hi']) |
        (bandwidth['lo'] & delay['hi'] & lossCount['lo']) |
        (bandwidth['lo'] & delay['hi'] & lossCount['md']) |
        (bandwidth['lo'] & delay['hi'] & lossCount['hi']) |
        (bandwidth['md'] & delay['md'] & lossCount['md']) |
        (bandwidth['md'] & delay['md'] & lossCount['hi']) |
        (bandwidth['md'] & delay['hi'] & lossCount['lo']) |
        (bandwidth['md'] & delay['hi'] & lossCount['md']) |
        (bandwidth['md'] & delay['hi'] & lossCount['hi']) |
        (bandwidth['hi'] & delay['hi'] & lossCount['hi'])
    ),
                      consequent=tip['lo'], label='rule ns')

    rule2 = ctrl.Rule(antecedent=(

        (bandwidth['md'] & delay['lo'] & lossCount['lo']) |
        (bandwidth['md'] & delay['lo'] & lossCount['md']) |
        (bandwidth['md'] & delay['lo'] & lossCount['hi']) |
        (bandwidth['md'] & delay['md'] & lossCount['lo']) |

        (bandwidth['hi'] & delay['lo'] & lossCount['hi']) |
        (bandwidth['hi'] & delay['md'] & lossCount['md']) |
        (bandwidth['hi'] & delay['md'] & lossCount['hi']) |
        (bandwidth['hi'] & delay['hi'] & lossCount['lo']) |
        (bandwidth['hi'] & delay['hi'] & lossCount['md'])
                    ),
                      consequent=tip['md'], label='rule ze')

    rule3 = ctrl.Rule(antecedent=(
        (bandwidth['hi'] & delay['lo'] & lossCount['lo']) |
        (bandwidth['hi'] & delay['lo'] & lossCount['md']) |
        (bandwidth['hi'] & delay['md'] & lossCount['lo'])

    ),
                      consequent=tip['hi'], label='rule ps')



    #system = ctrl.ControlSystem(rules=[rule1, rule2, rule3])

    #bandwidth.view()
    #delay.view()




    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    tipping.input['bandwidth'] = input1
    tipping.input['delay'] = input2
    tipping.input['lossCount'] = input3

    # Crunch the numbers
    tipping.compute()
    ############
    #print '###########',tipping.output['tip']
    return tipping.output['tip']

    #tip.view(sim=tipping)
def calc2(input1,input2,input3):

    x_hop = np.arange(0, 1000, 1)
    x_delay = np.arange(0, 600, 1)
    x_loss = np.arange(1, 11, 1)

    bandwidth = ctrl.Antecedent(x_hop, 'bandwidth')
    delay = ctrl.Antecedent(x_delay, 'delay')
    lossCount = ctrl.Antecedent(x_loss, 'lossCount')

    tip = ctrl.Consequent(np.arange(0, 11, 1), 'tip')

    names = ['lo', 'md', 'hi']

    #bandwidth.automf(names=names)
    #delay.automf(names=names)
    #tip.automf(names=names)
    # Generate fuzzy membership functions
    bandwidth['lo']= fuzz.trimf(x_hop, [0, 0, 400])  # (start,top,stop)
    bandwidth['md'] = fuzz.trimf(x_hop, [100, 500, 900])
    bandwidth['hi'] = fuzz.trimf(x_hop, [600, 1000, 1000])


    delay['lo']= fuzz.trimf(x_delay, [0, 0, 240])  # (start,top,stop)
    delay['md'] = fuzz.trimf(x_delay, [60, 300, 540])
    delay['hi']  = fuzz.trimf(x_delay, [360, 600, 600])


    lossCount['lo']= fuzz.trimf(x_loss, [0, 0, 4])  # (start,top,stop)
    lossCount['md'] = fuzz.trimf(x_loss, [1, 5, 9])
    lossCount['hi'] = fuzz.trimf(x_loss, [6, 10, 10])

    tip['lo'] = fuzz.trimf(tip.universe, [0, 0, 5])
    tip['md'] = fuzz.trimf(tip.universe, [0, 5, 11])
    tip['hi']  = fuzz.trimf(tip.universe, [5, 11, 11])


    rule1 = ctrl.Rule(antecedent=(
        (bandwidth['lo'] & delay['lo'] & lossCount['lo']) |
        (bandwidth['lo'] & delay['lo'] & lossCount['md']) |
        (bandwidth['lo'] & delay['lo'] & lossCount['hi']) |
        (bandwidth['lo'] & delay['md'] & lossCount['lo']) |
        (bandwidth['lo'] & delay['md'] & lossCount['md']) |
        (bandwidth['lo'] & delay['md'] & lossCount['hi']) |
        (bandwidth['lo'] & delay['hi'] & lossCount['lo']) |
        (bandwidth['lo'] & delay['hi'] & lossCount['md']) |
        (bandwidth['lo'] & delay['hi'] & lossCount['hi']) |
        (bandwidth['md'] & delay['md'] & lossCount['md']) |
        (bandwidth['md'] & delay['md'] & lossCount['hi']) |
        (bandwidth['md'] & delay['hi'] & lossCount['lo']) |
        (bandwidth['md'] & delay['hi'] & lossCount['md']) |
        (bandwidth['md'] & delay['hi'] & lossCount['hi']) |
        (bandwidth['hi'] & delay['hi'] & lossCount['hi'])
    ),
                      consequent=tip['lo'], label='rule ns')

    rule2 = ctrl.Rule(antecedent=(

        (bandwidth['md'] & delay['lo'] & lossCount['lo']) |
        (bandwidth['md'] & delay['lo'] & lossCount['md']) |
        (bandwidth['md'] & delay['lo'] & lossCount['hi']) |
        (bandwidth['md'] & delay['md'] & lossCount['lo']) |

        (bandwidth['hi'] & delay['lo'] & lossCount['hi']) |
        (bandwidth['hi'] & delay['md'] & lossCount['md']) |
        (bandwidth['hi'] & delay['md'] & lossCount['hi']) |
        (bandwidth['hi'] & delay['hi'] & lossCount['lo']) |
        (bandwidth['hi'] & delay['hi'] & lossCount['md'])
                    ),
                      consequent=tip['md'], label='rule ze')

    rule3 = ctrl.Rule(antecedent=(
        (bandwidth['hi'] & delay['lo'] & lossCount['lo']) |
        (bandwidth['hi'] & delay['lo'] & lossCount['md']) |
        (bandwidth['hi'] & delay['md'] & lossCount['lo'])

    ),
                      consequent=tip['hi'], label='rule ps')



    #system = ctrl.ControlSystem(rules=[rule1, rule2, rule3])

    #bandwidth.view()
    #delay.view()




    tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    tipping = ctrl.ControlSystemSimulation(tipping_ctrl)

    tipping.input['bandwidth'] = input1
    tipping.input['delay'] = input2
    tipping.input['lossCount'] = input3

    # Crunch the numbers
    tipping.compute()
    ############
    #print '###########',tipping.output['tip']
    return tipping.output['tip']

    #tip.view(sim=tipping)



if __name__ == '__main__':
    graph = Graph()

    print 'hxy',calc_hxy(1,2,10)
    print 'hxy',calc_hxy(2,2,10)

    print 'hxy',calc_hxy(3,2,10)
    print 'hxy',calc_hxy(5,2,10)
    print 'hxy',calc_hxy(7,2,10)
    print 'hxy',calc_hxy(9,2,10)
    print 'hxy',calc_hxy(10,2,10)

    print 'pxy',calc_pxy(200,100,1000)
    print 'pxy', calc_pxy(400, 100, 1000)
    print 'pxy', calc_pxy(600, 100, 1000)
    print 'pxy', calc_pxy(800, 100, 1000)

    for node in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
        graph.add_node(node)

    graph.add_edge('A', 'B', [400,20,1])
    graph.add_edge('A', 'C', [200,20,1])
    graph.add_edge('B', 'D', [300,20,1])
    graph.add_edge('C', 'D', [150,20,1])
    graph.add_edge('B', 'E', [450,20,1])
    graph.add_edge('D', 'E', [600,20,1])
    graph.add_edge('E', 'F',[700,20,1])
    graph.add_edge('F', 'G', [800,20,1])

    print graph.distances[('A','B' )][0]
    print graph.distances[('A','B' )]
    print(shortest_path(graph, 'A', 'B')) # output: (25, ['A', 'B', 'D'])
    print(shortest_path(graph, 'A', 'C')) # output: (25, ['A', 'B', 'D'])

    print(shortest_path(graph, 'A', 'D')) # output: (25, ['A', 'B', 'D'])
    print(shortest_path(graph, 'A', 'E')) # output: (25, ['A', 'B', 'D'])
    print(shortest_path(graph, 'A', 'F'))  # output: (25, ['A', 'B', 'D'])
    print(shortest_path(graph, 'A', 'G'))  # output: (25, ['A', 'B', 'D'])

#print(g.dijkstra(g, 'A')['B'])



# start_time = time.time()
#
# for i in range(100):
#     calc(300,100,7)
#
#
# print time.time()-start_time


# returns ({'a': 0}, {})