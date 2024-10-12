import numpy as np
import itertools as it
import pandas as pd


usecols = [
    'ranking_date',
    'rank',
    'player'
]


def load(association, cutoff):

    if association == 'atp':
        decades = [
            '70', '80', '90', '00', '10', '20'
        ]
    elif association == 'wta':
        decades = [
            '80', '90', '00', '10', '20'
        ]
    else:
        raise Exception('Association {0} not supported!'.format(association))

    files = [
        './tennis_{0}/{1}_rankings_{2}s.csv'.format(association, association, decade) for decade in decades
    ]

    rankings_df = pd.concat([pd.read_csv(file, usecols=['ranking_date', 'rank', 'player']) for file in files])
    rankings_df = rankings_df.rename(columns={'player': 'player_id'})

    players_file = './tennis_{0}/{1}_players.csv'.format(association, association)
    players_df = pd.read_csv(players_file, usecols=['player_id', 'name_first', 'name_last'])
    players_df['name'] = players_df['name_first'] + ' ' + players_df['name_last']
    players_df = players_df.drop(columns=['name_first', 'name_last'])

    df = pd.merge(rankings_df, players_df, on='player_id')

    df = df[df['rank'] <= cutoff]

    players_df = players_df.set_index('player_id')
    df['player_idx'], player_idx_to_id = pd.factorize(df['player_id'])
    player_idx_to_name = [players_df.loc[i]['name'] for i in player_idx_to_id]

    n = len(player_idx_to_id)
    rankings = []
    for _, grouped_df in df.groupby('ranking_date'):
        ranking = np.full(n, None)
        ranking[grouped_df['player_idx']] = grouped_df['rank']
        rankings.append(ranking)

    ranking_supp = np.array([
        [idx for idx in range(n) if ranking[idx] is not None] for ranking in rankings], dtype=list
    )
    player_supp_sz = np.array(
        [sum(1 for ranking in rankings if ranking[idx] is not None) for idx in range(n)], dtype=int
    )

    # plus one is added later in code
    w_mat = np.zeros((n, n))
    for k, ranking in enumerate(rankings):
        for i, j in it.permutations(ranking_supp[k], r=2):
            if ranking[i] < ranking[j]:
                w_mat[i, j] += player_supp_sz[i] / player_supp_sz[j]

    return w_mat, player_idx_to_id, player_idx_to_name
