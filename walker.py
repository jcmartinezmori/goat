import numpy as np
np.random.seed(0)


def main(w_mat, version, no_samples):

    w_mat += np.ones(w_mat.shape)

    if version == 'nonadj':
        mod = int(2 * (w_mat.shape[0] - 1))
        trans = np.array([(i, j) for i in range(w_mat.shape[0]) for j in range(i + 1, w_mat.shape[0])])
    elif version == 'adj':
        mod = int(2 * w_mat.shape[0] * (w_mat.shape[0] - 1) / 2)
        trans = np.array([(i, i + 1) for i in range(w_mat.shape[0] - 1)])
    else:
        raise Exception('Version {0} not supported!'.format(version))

    pis = []

    t, ct = 0, 0
    pi = np.random.permutation(np.array(range(w_mat.shape[0])))
    while ct < no_samples:
        t += 1
        if t % mod == 0:
            ct += 1
            pis.append(pi.copy())
            print('{0:.2f}%'.format(ct / no_samples * 100))
        pi = walk(trans, pi, w_mat)
    return pis


def walk(trans, pi, w_mat):
    if np.random.uniform() <= 0.5:
        p = [w_mat[pi[j], pi[i]] for i, j in trans]
        sum_p = sum(p)
        p = [p_ij / sum_p for p_ij in p]
        i, j = trans[np.random.choice(range(trans.shape[0]), p=p)]
        pi[i], pi[j] = pi[j], pi[i]
    return pi

