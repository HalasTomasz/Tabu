import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import json


def plotting(filename):
    data = json.load(open(filename, "r"))

    sym_data = []
    asym_data = []
    full_data = []
    eu_data = []

    types = [sym_data, asym_data, full_data, eu_data]

    for element in data:
        if element["Type"] == "sym":
            sym_data.append(element)
        elif element["Type"] == "asym":
            asym_data.append(element)
        elif element["Type"] == "full":
            full_data.append(element)
        elif element["Type"] == "eu":
            eu_data.append(element)

    for data_type in types:
        functions = [i["function"] for i in data_type]
        times = [i["time"] for i in data_type]
        solutions = [i["solution"] for i in data_type]
        tabu_sizes = [i["size_of tabu"] for i in data_type]
        graph_sizes = [i["size_of_graph"] for i in data_type]
        df = pd.DataFrame({'functions': functions, 'times': times, 'solutions': solutions, 'tabu_sizes': tabu_sizes,
                           'graph_sizes': graph_sizes})

        for graph_size in np.unique(graph_sizes):
            new_query = df.query(f"graph_sizes == {graph_size}")
            print(new_query)
            sns.lineplot(data=new_query, x='tabu_sizes', y='solutions', hue='functions')
            plt.title(f"Zależność rozwiązania od rozmiaru tabu dla grafu {data_type[0]['Type']}{graph_size}")
            plt.show()
            plt.clf()

        for tabu_size in np.unique(tabu_sizes):
            new_query = df.query(f"tabu_sizes == {tabu_size}")
            print(new_query)
            sns.lineplot(data=new_query, x='graph_sizes', y='times', hue='functions')
            plt.title(f"Zależność czasu od rozmiaru grafu {data_type[0]['Type']} dla tabu o rozmiarze {tabu_size}")
            plt.show()
            plt.clf()
