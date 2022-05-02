import ast
import sys
import random
import numpy as np
import copy 

def calc_dist(graph, permutation):
    dis = 0
    for i in range(0, len(permutation)):
        dis = dis + graph[permutation[i]][permutation[(i + 1) % len(permutation)]]['weight']
    return dis


def inversion(permutation, i, j):
    while i < j:
        swap(permutation, i, j)
        i += 1
        j -= 1
    return permutation


def swap(permutation, i, j):
    permutation[i], permutation[j] = permutation[j], permutation[i]
    return permutation


# def find(graph, permutation):
#     tabu_structure = {}
#
#     for i in range(0, graph.number_of_nodes()):
#         for j in range(i + 1, graph.number_of_nodes()):
#             current_object_value = inversion(permutation, i, j)
#             current_solution = calc_dist(graph, current_object_value)
#             tabu_structure[str(current_object_value)] = current_solution
#
#     tmp = {k: v for k, v in sorted(tabu_structure.items(), key=lambda item: item[1])}
#     return tmp


def find_neighbour_min(graph, permutation, tabu_list, neighbourhood_type):
    new_solution = permutation
    new_current_solution_cost = sys.maxsize
    current_i = 0
    current_j = 0

    for i in range(0, graph.number_of_nodes()):
        for j in range(i + 1, graph.number_of_nodes()):
            permutation = neighbourhood_type(permutation, i, j)
            current_solution_cost = calc_dist(graph, permutation)
            permutation = neighbourhood_type(permutation, j, i) ## Odkrecasz swapa ?
            if current_solution_cost < new_current_solution_cost and {i, j} not in tabu_list:
                new_solution = permutation
                new_current_solution_cost = current_solution_cost
                current_i = i
                current_j = j

    return new_solution, new_current_solution_cost, current_i, current_j

def find_neighbour_min_random(graph, permutation, tabu_list, neighbourhood_type):
    new_solution = copy.copy(permutation)
    new_current_solution_cost = sys.maxsize
    current_i = 0
    current_j = 0

    for i in range(0, graph.number_of_nodes()):
        for j in range(i + 1, graph.number_of_nodes()):
            permutation = neighbourhood_type(permutation, i, j)
            current_solution_cost = calc_dist(graph, permutation)
            if current_solution_cost < new_current_solution_cost and (permutation not in tabu_list):
                new_solution = copy.copy(permutation)
                new_current_solution_cost = current_solution_cost
                current_i = i
                current_j = j
            permutation = neighbourhood_type(permutation, j, i)
                
    return new_solution, new_current_solution_cost, current_i, current_j

def tabu_search(permutation, graph, number_of_iterations, tabu_size, neighbourhood_type, n_opt=1):
    count = 1
    solution = permutation
    tabu_list = list()
    best_cost = calc_dist(graph, permutation)
    best_solution_ever = solution
    best_solution_step = count

    while count <= number_of_iterations:
        if neighbourhood_type == "swap":
            solution, new_current_solution_cost, current_i, current_j = find_neighbour_min(graph, solution, tabu_list,
                                                                                           swap)
        elif neighbourhood_type == "invert":
            solution, new_current_solution_cost, current_i, current_j = find_neighbour_min(graph, solution, tabu_list,
                                                                                           inversion)
        #print(count, ": ", new_current_solution_cost)

        if new_current_solution_cost != sys.maxsize:
            #print(count, ": ", calc_dist(graph, solution))
            tabu_list.append({current_i, current_j})
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            if new_current_solution_cost < best_cost:
                best_solution_ever = solution
                best_cost = new_current_solution_cost
        else:
            current_i, current_j = tabu_list[-1][0], tabu_list[-1][1]
            solution[current_i], solution[current_j] = solution[current_j], solution[current_i]
        count += 1
    # while count <= number_of_iterations:
    #     neighborhood = find(graph, solution)
    #     counter = 0
    #     iterator = iter(neighborhood.items())
    #     tmp_pem, tmp_cost = next(iterator)
    #     tmp_pem = ast.literal_eval(tmp_pem)
    #     # print(tmp_cost)
    #     found = False
    #     while found is False:
    #
    #         # i = 0
    #         # first_exchange_node, second_exchange_node = [], []
    #         # n_opt_counter = 0
    #
    #         # while i < len(tmp_pem):
    #         #  if tmp_pem[i] != solution[i]:
    #         #    first_exchange_node.append(tmp_pem[i])
    #         #  second_exchange_node.append(solution[i])
    #         #  n_opt_counter += 1
    #         # if n_opt_counter == n_opt:
    #         #   break
    #         # i = i + 1
    #
    #         # exchange = first_exchange_node + second_exchange_node
    #         #  print(exchange)
    #         if len(tabu_list) > tabu_size:
    #             tabu_list.pop(0)
    #
    #         if tmp_pem not in tabu_list:
    #             tabu_list.append(tmp_pem)
    #             found = True
    #             solution = tmp_pem
    #             cost = tmp_cost
    #
    #             if cost < best_cost:
    #                 best_cost = cost
    #                 best_solution_ever = solution
    #
    #         elif counter < len(neighborhood):
    #             tmp_pem, tmp_cost = next(iterator)
    #             tmp_pem = ast.literal_eval(tmp_pem)
    #             counter += 1
    #
    #     while len(tabu_list) > tabu_size:
    #         solution = tabu_list.pop(0)
    #
    #     count += 1

    return best_solution_ever, best_cost


def tabu_search_random(permutation, graph, number_of_iterations, tabu_size, neighbourhood_type, n_opt=1):
    
    count = 1
    solution = permutation
    tabu_list = list()
    best_cost = calc_dist(graph, permutation)
    best_solution_ever = solution
    best_solution_step = count

    while count <= number_of_iterations:
    
        if neighbourhood_type == "swap":
            solution, new_current_solution_cost, _, _ = find_neighbour_min_random(graph, solution, tabu_list, swap)
        elif neighbourhood_type == "invert":
            solution, new_current_solution_cost, _, _ = find_neighbour_min_random(graph, solution, tabu_list,inversion)
        
        print(new_current_solution_cost)
        #print(count, ": ", new_current_solution_cost)

        if new_current_solution_cost != sys.maxsize:
            #print(count, ": ", calc_dist(graph, solution))
            
            tabu_list.append(solution)
            
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
                
            if new_current_solution_cost < best_cost:
                best_solution_ever = solution
                best_cost = new_current_solution_cost
        else:
            
            random.shuffle(solution)
            
        count += 1
   
    return best_solution_ever, best_cost
