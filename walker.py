import numpy as np
np.random.seed(0)


def main(w_mat, no_samples=100000, mod=1):

    w_mat += np.ones(w_mat.shape)

    trans = np.array([(i, j) for i in range(w_mat.shape[0]) for j in range(i, w_mat.shape[0])])
    pis = []

    t, ct = 0, 0
    pi = np.random.permutation(np.array(range(w_mat.shape[0])))
    while ct < no_samples:
        t += 1
        if t % mod == 0:
            ct += 1
            pis.append(pi.copy())
            # print('{0:.2f}%'.format(ct / no_samples * 100))
        pi = walk(trans, pi, w_mat)
    return pis


def walk(trans, pi, w_mat):
    i, j = propose(trans, pi, w_mat)
    pi[i], pi[j] = pi[j], pi[i]
    return pi


def propose(trans, pi, w_mat):
    p = [w_mat[i, j] if pi[i] > pi[j] else w_mat[j, i] for i, j in trans]
    sum_p = sum(p)
    p = [p_ij / sum_p for p_ij in p]
    i, j = trans[np.random.choice(range(trans.shape[0]), p=p)]
    return i, j
