import ast
import sys
import copy


def calc_dist(graph, permutation):
    dis = 0
    for i in range(0, len(permutation)):
        dis = dis + graph[permutation[i]][permutation[(i + 1) % len(permutation)]]['weight']
    return dis


def inversion(permutation, m, n):
    new_permutation = []
    for i in range(0, m + 1):
        new_permutation.append(permutation[i])
    for i in range(n, m, -1):
        new_permutation.append(permutation[i])
    for i in range(n + 1, len(permutation)):
        new_permutation.append(permutation[i])
    return new_permutation


def calc_inversion_dist(graph, permutation, i, j):
    dist = 0
    # todo
    return dist



# def inversion(permutation, m, n):
#     solution = copy.deepcopy(permutation)
#     while m < n:
#         swap_move(solution, m, n)
#         m += 1
#         n -= 1
#     return solution


def swap_move(permutation, i, j):
    permutation[i], permutation[j] = permutation[j], permutation[i]
    return permutation


def find(graph, permutation):
    tabu_structure = {}

    for i in range(0, graph.number_of_nodes()):
        for j in range(i + 1, graph.number_of_nodes()):
            current_object_value = inversion(permutation, i, j)
            current_solution = calc_dist(graph, current_object_value)
            tabu_structure[str(current_object_value)] = current_solution

    tmp = {k: v for k, v in sorted(tabu_structure.items(), key=lambda item: item[1])}
    return tmp


def find_neighbour_min(graph, permutation, tabu_list):
    solution = copy.deepcopy(permutation)
    new_current_solution_cost = sys.maxsize
    current_i = 0
    current_j = 0

    for i in range(0, graph.number_of_nodes()):
        for j in range(i + 1, graph.number_of_nodes()):
            neighbour = inversion(permutation, i, j)
            current_solution_cost = calc_dist(graph, neighbour)
            if current_solution_cost < new_current_solution_cost and (i, j) not in tabu_list:
                solution = neighbour
                new_current_solution_cost = current_solution_cost
                current_i = i
                current_j = j

    return solution, new_current_solution_cost, current_i, current_j


def tabu_search(permutation, graph, number_of_iterations, tabu_size, n_opt=1):
    count = 1
    solution = copy.deepcopy(permutation)
    tabu_list = list()
    best_cost = calc_dist(graph, permutation)
    best_solution_ever = solution

    while count <= number_of_iterations:
        print(count)
        neighbour, new_current_solution_cost, current_i, current_j = find_neighbour_min(graph, solution, tabu_list)

        if new_current_solution_cost != sys.maxsize:
            tabu_list.append((current_i, current_j))
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)
            if new_current_solution_cost < best_cost:
                best_solution_ever = neighbour
                best_cost = new_current_solution_cost
        else:
            print("ups")
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
