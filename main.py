import helper as hp
import joblib as jb
import itertools as it
import pandas as pd
import pickle
import walker as wk


def main(association, max_rank, no_samples=100000, version='v2'):

    w_mat, player_idx_to_id, player_idx_to_name = hp.loadv2(association, max_rank)

    mod = w_mat.shape[0] if w_mat.shape[0] % 2 else w_mat.shape[0] + 1
    pis = wk.main(w_mat, no_samples=no_samples, mod=mod)

    out = pd.DataFrame(pis, columns=player_idx_to_name)
    out += 1
    med = out.median()
    med = med.sort_values()
    out = out[med.index]

    with open('./results/{0}_player_idx_to_id_{1}-{2}.pkl'.format(version, association, max_rank), 'wb') as file:
        pickle.dump(player_idx_to_id, file)
    with open('./results/{0}_player_idx_to_name_{1}-{2}.pkl'.format(version, association, max_rank), 'wb') as file:
        pickle.dump(player_idx_to_name, file)
    out.to_csv('./results/{0}_out_{1}-{2}.csv'.format(version, association, max_rank), index=False)


if __name__ == '__main__':

    ver = 2
    sam = 100000
    association_l = ['atp', 'wta']
    max_rank_l = [3, 5, 10, 20]

    jobs = [(association, max_rank, sam) for association, max_rank in it.product(association_l, max_rank_l)]
    jb.Parallel(n_jobs=8, verbose=11)(jb.delayed(main)(*job) for job in jobs)
