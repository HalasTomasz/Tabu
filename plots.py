import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import json, operator


# %%
def count_spec(df, names):
    all_results = []
    for name in names:
        name_df = df[df['function'] == name]
        city_names = ["burma14.tsp", "bayg29.tsp", "bays29.tsp", "att48.tsp", "berlin52.tsp", "bier127.tsp", "ch130.tsp"]
        city_sizes = [14, 29, 29, 48, 52, 127, 130]
        for i in range(len(city_names)):
            test_df = name_df[name_df['Type'] == city_names[i]].agg(['min', 'max', 'mean', 'std'])
            result_dist = {'name': city_names[i],
                           'size': city_sizes[i],
                           'function': name,
                           'min_dist': test_df.min()['solution'],
                           'max_dist': test_df.max()['solution'],
                           'mean_dist': test_df.mean()['solution'],
                           'std_dist': test_df.std()['solution'],
                           'min_time': test_df.min()['time'],
                           'max_time': test_df.max()['time'],
                           'mean_time': test_df.mean()['time'],
                           'std_time': test_df.std()['time'], }
            all_results.append(result_dist)
    return pd.DataFrame(all_results)


df_Data = pd.read_json(r'towns_opt_swap.json')

names = ['tabu_ex_inv', 'tabu_ex_swap', 'tabu_opt_invert', 'tabu_opt_r_invert', 'tabu_r_invert']
df_3_agg = count_spec(df_Data, names)

# %%
sns.lineplot(data=df_3_agg, x='name', y='mean_dist', hue='function')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.show()
plt.clf()

# %%

# sns.barplot(data=sym_data.loc[sym_data['function'] == 'tabu_ex_swap'], x='size_of tabu', y='size_of_graph',
#             hue='solution')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.show()
# plt.clf()
