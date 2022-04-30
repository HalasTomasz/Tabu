import os
import function_module
import tsplib95
import networkx as nx
import glob
import json
import time
import Tabu
import numpy as np
"""
def test from given path 
use it to open and solve tests
"""

def test(path):
    
    print(path)
    
    collector = []
    size_of_tabu_table = [10,50,100,200,500,1000]
    node_NN = 1
    file_number = 0
    for filename in os.listdir(path):
        file_number += 1
        if file_number > 20:
            break
        # print(filename)

        path_to_folder = path + "/" + filename
        path_to_tsp = r"" + path + "/" + filename + '/' + filename
        answer = set([os.path.dirname(p) for p in glob.glob(path_to_folder + "/*/*")])

        assert os.path.isfile(path_to_tsp)
        with open(path_to_tsp, "r") as f:

            print("Solving :" + filename)
            problem = tsplib95.read(f)
            graph = problem.get_graph()
            graph = graph.to_directed()

            if answer:
                path_to_tour = path_to_folder + "/" + filename.split('.')[0] + ".opt.tour" + "/" + filename.split('.')[0] + ".opt.tour"
                opt = tsplib95.load(path_to_tour)
                print("Rozwiązanie optymalne: ", problem.trace_tours(opt.tours))
            else:
                opt = "None"
                
            for size in size_of_tabu_table:
                 
                 """
                 EXTENTED TABU SEARCH WITH INV
                 """
             
                 starting_permuation = function_module.extended_nearest_neighbour(graph)[0]  # Staring Permuataion
                 
                 start = time.process_time()
                 
             
                 permutation, cost = Tabu.tabu_search(starting_permuation, graph, size, len(starting_permuation)) # Run Tabu
                 
                 end = time.process_time()
                 
                 collector.append(DataGraph(filename,'tabu_ex_inv',end-start, cost,str(permutation),size,"None"))
                 
                 ## Dodałbys prosze tabu ze swapem?
                 """
                 EXTENTED TABU SEARCH WITH SWAP
                 """
                       
                 
                 
                 """
                 OPT2 [1,2,3....n] TABU SEARCH WITH SWAP/INV?
                 """
                 
                 opt2Permuation = list(range(1, graph.number_of_nodes() + 1))
                 
                 starting_permuation = function_module.OPT2(graph,opt2Permuation)[0]
                 
                 start = time.process_time()
                 
                 permutation, cost = Tabu.tabu_search(starting_permuation, graph, size, len(starting_permuation))
                 
                   
                 end = time.process_time()
                 
                 collector.append(DataGraph(filename,'tabu_opt_inv',end-start, cost,str(permutation),size,"None"))
                 
                 """
                 OPT2 [random] TABU SEARCH WITH SWAP/INV?
                 """
                 
                 opt2Permuation = list(range(1, graph.number_of_nodes() + 1))
                 np.random.shuffle(opt2Permuation)
                 
                 starting_permuation = function_module.OPT2(graph,opt2Permuation)[0]
                 
                 start = time.process_time()
                 
                 permutation, cost = Tabu.tabu_search(starting_permuation, graph, size, len(starting_permuation))
                 
                 end = time.process_time()
                 
                 collector.append(DataGraph(filename,'tabu_opt_r_swap>>>>',end-start, cost,str(permutation),size,"None")) ## ZOBACZ TU!!
                 
                 """
                 My random tabu search
                 """
          
                
    try:
        with open('C:/Users/denev/TSP/files7.json', 'w') as fout:
            json.dump(collector , fout)
    except IOError:
        pass
    finally:
        fout.close()


"""
dic to save data to JSON 
"""


def DataGraph(Type, func, time, solution, permutation,tabu, opt ):
    Dic = {
        'Type': Type,
        'function': func,
        'time': time,
        'solution': solution,
        'size_of tabu': tabu,
        'optimal_solution': opt
        # 'memory'

    }
    return Dic


# def generate_graph(n, seed, type_of_problem):

"""
tests on auto generated graph
"""


def test_auto_generate(seed=100):
    types = ['sym', 'asym', 'full' 'eu']  
    collection = []
    size_of_tabu_table = [10,50,100,200,500,1000]
    
    for i in range(1,10):
        
        for n in range(10, 300, 20):
            
            for graph_type in types:
                
                for size in size_of_tabu_table:
                    
                    """
                    EXTENTED TABU SEARCH WITH INV
                    """
                
                    graph = function_module.generate_graph(n, seed, graph_type) #Create graph
                    
                    starting_permuation = function_module.extended_nearest_neighbour(graph)[0]  # Staring Permuataion
                    
                    start = time.process_time()
                    
                
                    permutation, cost = Tabu.tabu_search(starting_permuation, graph, size, len(starting_permuation)) # Run Tabu
                    
                    end = time.process_time()
                    
                    collection.append(DataGraph(graph_type,'tabu_ex_inv',end-start, cost,str(permutation),size,"None"))
                    
                    ## Dodałbys prosze tabu ze swapem?
                    """
                    EXTENTED TABU SEARCH WITH SWAP
                    """
                         
                    
                    
                    """
                    OPT2 [1,2,3....n] TABU SEARCH WITH SWAP/INV?
                    """
                    
                    opt2Permuation = list(range(1, graph.number_of_nodes() + 1))
                    
                    starting_permuation = function_module.OPT2(graph,opt2Permuation)[0]
                    
                    start = time.process_time()
                    
                    permutation, cost = Tabu.tabu_search(starting_permuation, graph, size, len(starting_permuation))
                    
                      
                    end = time.process_time()
                    
                    collection.append(DataGraph(graph_type,'tabu_opt_inv',end-start, cost,str(permutation),size,"None"))
                    
                    """
                    OPT2 [random] TABU SEARCH WITH SWAP/INV?
                    """
                    
                    opt2Permuation = list(range(1, graph.number_of_nodes() + 1))
                    np.random.shuffle(opt2Permuation)
                    
                    starting_permuation = function_module.OPT2(graph,opt2Permuation)[0]
                    
                    start = time.process_time()
                    
                    permutation, cost = Tabu.tabu_search(starting_permuation, graph, size, len(starting_permuation))
                    
                    end = time.process_time()
                    
                    collection.append(DataGraph(graph_type,'tabu_opt_r_swap>>>>',end-start, cost,str(permutation),size,"None")) ## ZOBACZ TU!!
                    
                    """
                    My random tabu search
                    """
    


    try:
        file = open("Final_test2", "w")
        json.dump(collection, file, indent=3)
    except IOError:
        pass
    finally:
        file.close()
