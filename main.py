import math
import networkx as nx
import numpy as np
import random
import function_module
import Tabu
import copy
import tsplib95
import time

import plots
import testing
import plotting


def read_graph_input(file):
    with open(file) as f:
        problem = tsplib95.read(f)

    new_graph = problem.get_graph()
    new_graph = new_graph.to_directed()

    opt = tsplib95.load('bays29.opt.tour')
    print(problem.trace_tours(opt.tours))
    return new_graph


if __name__ == '__main__':
    #graph = read_graph_input('bays29.tsp')
    """
    Create random soluton to begin with
    """
    # np.random.seed(100)
    # start = np.array(range(1, graph.number_of_nodes() + 1))
    # np.random.shuffle(start)
    # start = list(start)
    # print(function_module.OPT2(graph, start))

    #start = function_module.extended_nearest_neighbour(graph)[0]
    #print(function_module.extended_nearest_neighbour(graph)[1])
    #print(start)
    #print(Tabu.tabu_search(start, graph, 1000, 10, "swap"))
    #print(start)
    #print(Tabu.tabu_search_random(copy.copy(start), graph, 50, 10, "swap"))
    #print(start)
    #print(Tabu.tabu_search(start, graph, math.pow(len(start), 2), len(start)))

    # """
    # Create random using OPT2
    # """
    # start,_ = function_module.OPT2(graph)
    # testing.test("C:/Users/szyme/PycharmProjects/Tabu/Data_Meta", "invert")

    plots.count_spec()
