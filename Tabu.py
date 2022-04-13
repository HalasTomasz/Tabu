import ast

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


def SwapMove(permutation, i ,j):

     solution = []
     permutation[i], permutation[j] = permutation[j], permutation[i]
     solution = permutation
     return solution

def Find(G,permutation):
    tabu_structure = {}
    
    for i in range(0, G.number_of_nodes()):
         for j in range(i + 1, G.number_of_nodes()):
            
            current_objvalue = inversion(permutation, i, j)
            current_solution = calc_dist(G,current_objvalue)
            tabu_structure[str(current_objvalue)] = current_solution
            
    tmp = {k: v for k, v in sorted(tabu_structure.items(), key=lambda item: item[1])}
    return tmp

def tabu_search(permutation, G, iters, size, n_opt=1):
    
    count = 1
    solution = permutation
    tabu_list = list()
    best_cost = calc_dist(G, permutation) 
    best_solution_ever = solution
    
    while count <= iters:
       # print(count)
        neighborhood = Find(G, solution)
        counter = 0
        iterator = iter(neighborhood.items())
        tmp_pem,tmp_cost= next(iterator)
        tmp_pem = ast.literal_eval(tmp_pem)
        #print(tmp_cost)
        found = False
        while found is False:
            
           # i = 0
           # first_exchange_node, second_exchange_node = [], []
           # n_opt_counter = 0
            
           # while i < len(tmp_pem):
              #  if tmp_pem[i] != solution[i]:
                #    first_exchange_node.append(tmp_pem[i])
                  #  second_exchange_node.append(solution[i])
                 #  n_opt_counter += 1
                   # if n_opt_counter == n_opt:
                     #   break
               # i = i + 1

           # exchange = first_exchange_node + second_exchange_node
          #  print(exchange)
            if len(tabu_list) > size:
                tabu_list.pop(0)

            if tmp_pem not in tabu_list:
                tabu_list.append(tmp_pem)
                found = True
                solution = tmp_pem
                cost = tmp_cost
                
                if cost < best_cost:
                    best_cost = cost
                    best_solution_ever = solution
                    
            elif counter < len(neighborhood):
                tmp_pem,tmp_cost= next(iterator)
                tmp_pem = ast.literal_eval(tmp_pem)
                counter = counter + 1

                    
        while len(tabu_list) > size:
            solution = tabu_list.pop(0)
            

        count = count + 1

    return best_solution_ever, best_cost
