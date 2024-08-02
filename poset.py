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

    n = len(player_idx_to_id)
    out = out.iloc[10000:]

    mu = np.zeros((n, n))
    for i in range(n):
        name = player_idx_to_name[i]
        for r in out[name] - 1:
            # mu[i][r] += 1
            mu[r, i] += 1
    mu = mu / mu.sum(axis=1)
    # mu = mu / mu.sum(axis=1)

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

    ver_l = ['adj', 'nonadj']
    assc_l = ['wta', 'atp']
    ctff_l = [20]

    for ver in ver_l:
        for assc in assc_l:
            for ctff in ctff_l:
                main(ver, assc, ctff)

