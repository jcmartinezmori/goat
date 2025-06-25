import numpy as np
import itertools as it
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"


colors = {
    'white': '#ffffff',
    'black': '#000000',
    'orange': '#e69f00',
    'skyblue': '#56b4e9',
    'bluishgreen': '#009e73',
    'yellow': '#f0e442',
    'blue': '#0072b2',
    'vermillion': '#d55e00',
    'reddishpurple': '#cc79a7'
}

usecols = [
    'ranking_date',
    'rank',
    'player'
]


def main(association, cutoff, plot_cutoff):

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

    counts = df['name'].value_counts().head(plot_cutoff)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=counts.index,
        y=counts.values,
        mode='markers+lines',
        marker=dict(
            color=colors['orange'] if association == 'atp' else colors['blue'],
            symbol='circle' if association == 'atp' else 'square'
        ),
    ))
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Number of Weeks',
        yaxis_range=[0, 1200 + 2],
        margin=dict(b=10, l=10, r=10, t=10),
        xaxis=dict(autorange='reversed')
    )

    fig.write_image(
        './weeks/weeks_{0}-{1}-{2}.pdf'.format(association, cutoff, plot_cutoff),
        width=1200, height=325, scale=1
    )


if __name__ == '__main__':

    assc_l = ['wta', 'atp']
    ctff_l = [3, 5, 10, 20]
    plt_ctff_l = [20]

    for assc in assc_l:
        for ctff in ctff_l:
            for plt_ctff in plt_ctff_l:
                main(assc, ctff, plt_ctff)
