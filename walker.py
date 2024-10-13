import numpy as np
np.random.seed(0)


def main(w_mat, version, no_samples):

    n = w_mat.shape[0]
    if version == 'nonadj':
        mod = int(2 * 1/2 * n * np.log(n))
        trans = np.array([(i, j) for i in range(n) for j in range(i + 1, n)])
    elif version == 'adj':
        mod = int(2 / (np.pi ** 2) * (n ** 3) * np.log(n))
        trans = np.array([(i, i + 1) for i in range(n - 1)])
    else:
        raise Exception('Version {0} not supported!'.format(version))

    pis = []

    t, ct = 0, 0
    pi = np.random.permutation(np.array(range(n)))
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
        if np.random.uniform() <= 0.5:
            p = [w_mat[j, i] if pi[i] < pi[j] else w_mat[i, j] for i, j in trans]
            sum_p = sum(p)
            p = [p_ij / sum_p for p_ij in p]
            i, j = trans[np.random.choice(range(trans.shape[0]), p=p)]
        else:
            i, j = trans[np.random.choice(range(trans.shape[0]))]
        pi[i], pi[j] = pi[j], pi[i]
    return pi

