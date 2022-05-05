import os
import function_module
import tsplib95
import networkx as nx
import copy
import glob
import json
import time
import Tabu
import numpy as np
import re

"""
def test from given path 
use it to open and solve tests
"""


def test(path, neighbourhood_type):
    print(path)

    collector = []
    size_of_tabu_table = [10, 50, 100, 200, 500]
    node_NN = 1
    file_number = 0
    for filename in os.listdir(path):
        file_number += 1
        if file_number > 7:
            break
        # print(filename)

        path_to_folder = path + "/" + filename
        path_to_tsp = r"" + path + "/" + filename + '/' + filename
        answer = set([os.path.dirname(p) for p in glob.glob(path_to_folder + "/*/*")])
        n = int(re.findall(r'\d+', filename)[0])
        print(n)

        assert os.path.isfile(path_to_tsp)
        with open(path_to_tsp, "r") as f:

            print("Solving :" + filename)
            problem = tsplib95.read(f)
            graph = problem.get_graph()
            graph = graph.to_directed()

            if answer:
                path_to_tour = path_to_folder + "/" + filename.split('.')[0] + ".opt.tour" + "/" + filename.split('.')[
                    0] + ".opt.tour"
                opt = tsplib95.load(path_to_tour)
                opt = opt.tours
                print("Rozwiązanie optymalne: ", problem.trace_tours(opt))
            else:
                opt = "None"

            for m in range(2):
                for size in size_of_tabu_table:
                    # """
                    #  EXTENDED TABU SEARCH WITH INV
                    #  """
                    #
                    # starting_permutation = function_module.extended_nearest_neighbour(graph)[0]  # Staring Permutation
                    #
                    # start = time.process_time()
                    #
                    # permutation, cost = Tabu.tabu_search(starting_permutation, graph, size, len(starting_permutation),
                    #                                      "invert")  # Run Tabu
                    #
                    # end = time.process_time()
                    #
                    # collector.append(DataGraph(filename, 'tabu_ex_inv', end - start, cost, str(permutation), size, n, opt))
                    #
                    # """
                    #  EXTENDED TABU SEARCH WITH SWAP
                    #  """
                    #
                    # starting_permutation = function_module.extended_nearest_neighbour(graph)[0]  # Staring Permutation
                    #
                    # start = time.process_time()
                    #
                    # permutation, cost = Tabu.tabu_search(starting_permutation, graph, size, len(starting_permutation),
                    #                                      "swap")  # Run Tabu
                    #
                    # end = time.process_time()
                    #
                    # collector.append(DataGraph(filename, 'tabu_ex_swap', end - start, cost, str(permutation), size, n, opt))

                    """
                     OPT2 [1,2,3....n] TABU SEARCH WITH INV/SWAP
                     """

                    opt2Permutation = list(range(1, graph.number_of_nodes() + 1))

                    starting_permutation = function_module.OPT2(graph, opt2Permutation)[0]

                    start = time.process_time()

                    permutation, cost = Tabu.tabu_search(starting_permutation, graph, size, len(starting_permutation),
                                                         neighbourhood_type)

                    end = time.process_time()

                    collector.append(DataGraph(filename, 'tabu_opt_' + neighbourhood_type, end - start, cost,
                                               str(permutation), size, n, opt))

                    """
                     OPT2 [random] TABU SEARCH WITH INV/SWAP
                     """

                    opt2Permutation = list(range(1, graph.number_of_nodes() + 1))
                    np.random.shuffle(opt2Permutation)

                    starting_permutation = function_module.OPT2(graph, opt2Permutation)[0]

                    start = time.process_time()

                    permutation, cost = Tabu.tabu_search(starting_permutation, graph, size, len(starting_permutation),
                                                         neighbourhood_type)

                    end = time.process_time()

                    collector.append(DataGraph(filename, 'tabu_opt_r_' + neighbourhood_type, end - start, cost,
                                               str(permutation), size, n, opt))

                    """
                     My random tabu search
                     """
                    starting = function_module.extended_nearest_neighbour(graph)[0]

                    start = time.process_time()

                    permutation, cost = Tabu.tabu_search_random(copy.copy(starting), graph, size,
                                                                len(starting_permutation),
                                                                neighbourhood_type)
                    end = time.process_time()
                    collector.append(
                        DataGraph(filename, 'tabu_r_' + neighbourhood_type, end - start, cost, str(permutation), size,
                                  n, opt))
    try:
        with open('C:/Users/szyme/PycharmProjects/Tabu/towns_opt_invert', 'w') as fout:
            json.dump(collector, fout)
    except IOError:
        pass
    finally:
        fout.close()


"""
dic to save data to JSON 
"""


def DataGraph(Type, func, t, solution, permutation, tabu, n, opt):
    Dic = {
        'Type': Type,
        'function': func,
        'time': t,
        'solution': solution,
        'size_of tabu': tabu,
        'size_of_graph': n,
        'optimal_solution': opt
        # 'memory'

    }
    return Dic


# def generate_graph(n, seed, type_of_problem):

"""
tests on auto generated graph
"""


def test_auto_generate(seed=100, neighbourhood_type="invert"):
    types = ['sym', 'asym']
    collection = []
    size_of_tabu_table = [10, 50, 100, 200]  # 500 and 10000

    for i in range(3):  # 10

        for n in range(10, 150, 20):  # 300
            for graph_type in types:

                for size in size_of_tabu_table:
                    """
                    EXTENDED TABU SEARCH WITH INV
                    """

                    graph = function_module.generate_graph(n, seed, graph_type)  # Create graph

                    starting_permutation = function_module.extended_nearest_neighbour(graph)[0]  # Staring Permutation

                    start = time.process_time()

                    permutation, cost = Tabu.tabu_search(starting_permutation, graph, size,
                                                         len(starting_permutation), "invert")  # Run Tabu

                    end = time.process_time()

                    collection.append(
                        DataGraph(graph_type, 'tabu_ex_inv', end - start, cost, str(permutation), size, n, "None"))

                    """
                    EXTENDED TABU SEARCH WITH SWAP
                    """

                    # graph = function_module.generate_graph(n, seed, graph_type)  # Create graph

                    starting_permutation = function_module.extended_nearest_neighbour(graph)[0]  # Staring Permutation

                    start = time.process_time()

                    permutation, cost = Tabu.tabu_search(starting_permutation, graph, size,
                                                         len(starting_permutation), "swap")  # Run Tabu

                    end = time.process_time()

                    collection.append(
                        DataGraph(graph_type, 'tabu_ex_swap', end - start, cost, str(permutation), size, n, "None"))

                    # """
                    # OPT2 [1,2,3....n] TABU SEARCH WITH INV/SWAP
                    # """
                    #
                    # opt2Permutation = list(range(1, graph.number_of_nodes() + 1))
                    #
                    # starting_permutation = function_module.OPT2(graph, opt2Permutation)[0]
                    #
                    # start = time.process_time()
                    #
                    # permutation, cost = Tabu.tabu_search(starting_permutation, graph, size, len(starting_permutation),
                    #                                      neighbourhood_type)
                    #
                    # end = time.process_time()
                    #
                    # collection.append(
                    #     DataGraph(graph_type, 'tabu_opt_' + neighbourhood_type, end - start, cost,str(permutation),
                    #               size,n, "None"))
                    #
                    #
                    # """
                    # OPT2 [random] TABU SEARCH WITH INV/SWAP
                    # """
                    #
                    # opt2Permutation = list(range(1, graph.number_of_nodes() + 1))
                    # np.random.shuffle(opt2Permutation)
                    #
                    # starting_permutation = function_module.OPT2(graph, opt2Permutation)[0]
                    #
                    # start = time.process_time()
                    #
                    # permutation, cost = Tabu.tabu_search(starting_permutation, graph, size, len(starting_permutation),
                    #                                      neighbourhood_type)
                    #
                    # end = time.process_time()
                    #
                    # collection.append(
                    #     DataGraph(graph_type, 'tabu_opt_r_' + neighbourhood_type, end - start, cost, str(permutation),
                    #               size, n,"None"))

                    """
                    My random tabu search
                    """
                    starting = function_module.extended_nearest_neighbour(graph)[0]

                    start = time.process_time()

                    permutation, cost = Tabu.tabu_search_random(copy.copy(starting), graph, size,
                                                                len(starting_permutation),
                                                                neighbourhood_type)
                    end = time.process_time()
                    collection.append(
                        DataGraph(graph_type, 'tabu_r_' + neighbourhood_type, end - start, cost, str(permutation), size,
                                  n, "None"))

            print("finish " + str(n))
    try:
        file = open("Final_result_10_200", "w")
        json.dump(collection, file, indent=3)
    except IOError:
        pass
    finally:
        file.close()
