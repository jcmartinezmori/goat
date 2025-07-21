import numpy as np
np.random.seed(0)


def main(w_mat, version, no_samples):

    w_mat += np.ones(w_mat.shape) / (w_mat.shape[0] ** 2)

    if version == 'nonadj':
        mod = int(2 * (w_mat.shape[0] - 1))
        trans = np.array([(i, j) for i in range(w_mat.shape[0]) for j in range(i + 1, w_mat.shape[0])])
        trans_supp = np.array([
            {(idx, (i, j)) for idx, (i, j) in enumerate(trans) if i == h or j == h} for h in range(w_mat.shape[0])
        ])
        supp = np.empty(w_mat.shape, dtype=object)
        for i in range(w_mat.shape[0]):
            for j in range(i + 1, w_mat.shape[0]):
                supp[i, j] = set.union(trans_supp[i],trans_supp[j])
    else:
        raise Exception('Version {0} not supported!'.format(version))

    t, ct = 0, 0
    pi = np.random.permutation(np.array(range(w_mat.shape[0])))
    p = np.array([w_mat[pi[j], pi[i]] for i, j in trans])
    p_sum = p.sum()

    pis = np.empty((no_samples, *pi.shape), dtype=pi.dtype)

    while ct < no_samples:
        t += 1
        if t % mod == 0:
            pis[ct] = pi
            ct += 1
            if ct % 1000 == 0:
                print('{0:.2f}%'.format(ct / no_samples * 100))
        pi, p, p_sum = walk(pi, p, p_sum, w_mat, trans, supp)
    return pis


# def walk(trans, pi, w_mat):
#     if np.random.uniform() <= 0.5:
#         p = [w_mat[pi[j], pi[i]] for i, j in trans]
#         sum_p = sum(p)
#         p = [p_ij / sum_p for p_ij in p]
#         i, j = trans[np.random.choice(range(trans.shape[0]), p=p)]
#         pi[i], pi[j] = pi[j], pi[i]
#     return pi


def walk(pi, p, p_sum, w_mat, trans, supp):
    if np.random.uniform() <= 0.5:
        p /= p_sum
        i_star, j_star = trans[np.random.choice(range(trans.shape[0]), p=p)]
        p *= p_sum
        pi[i_star], pi[j_star] = pi[j_star], pi[i_star]
        for idx, (i, j) in supp[i_star, j_star]:
            val = w_mat[pi[j], pi[i]]
            p_sum += val - p[idx]
            p[idx] = val

    return pi, p, p_sum
