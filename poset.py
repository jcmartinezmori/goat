import itertools as it
import networkx as nx
import numpy as np
import pandas as pd
import pickle


def main(version, association, cutoff):

    with open('./results/{0}_player_idx_to_id_{1}-{2}.pkl'.format(version, association, cutoff), 'rb') as file:
        player_idx_to_id = pickle.load(file)
    with open('./results/{0}_player_idx_to_name_{1}-{2}.pkl'.format(version, association, cutoff), 'rb') as file:
        player_idx_to_name = pickle.load(file)
    out = pd.read_csv('./results/{0}_out_{1}-{2}.csv'.format(version, association, cutoff))
    out.columns = out.columns.astype(int)

    n = out.shape[1]

    arr = out.to_numpy() - 1
    rows = arr.flatten()
    cols = np.tile(np.arange(n), len(arr))
    mu = np.zeros((n, n), dtype=int)
    np.add.at(mu, (rows, cols), 1)

    g = nx.DiGraph()
    g.add_nodes_from(range(n))
    for i, j in it.permutations(range(n), r=2):
        if all(sum(mu[i][:r]) >= sum(mu[j][:r]) for r in range(n)):
            g.add_edge(i, j)
    g = nx.transitive_reduction(g)
    for dist, nodes in enumerate(nx.topological_generations(g)):
        for i in nodes:
            g.nodes[i]['dist'] = dist
            g.nodes[i]['player_name'] = player_idx_to_name[i]
            g.nodes[i]['player_id'] = player_idx_to_id[i]

    with open('./poset/poset_{0}-{1}-{2}.pkl'.format(version, association, cutoff), 'wb') as file:
        pickle.dump(g, file)


if __name__ == '__main__':

    ver_l = ['nonadj']
    assc_l = ['atp', 'wta']
    ctff_l = [3, 5]

    for ver in ver_l:
        for assc in assc_l:
            for ctff in ctff_l:
                main(ver, assc, ctff)
