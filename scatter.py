import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
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


def main(version, association, cutoff_l, plot_cutoff):

    df = None
    for cutoff in cutoff_l:
        r_df = pd.read_csv(
            './extension/extension_{0}-{1}-{2}.csv'.format(version, association, cutoff),
            usecols=['player_name', 'player_id', 'avg_rank']
        )
        r_df = r_df.rename(columns={'avg_rank': 'avg_rank_{0}'.format(cutoff)})
        r_df = r_df[:plot_cutoff]
        if df is None:
            df = r_df
        else:
            df = pd.merge(df, r_df, on=['player_id', 'player_name'], how='outer')
    df = df.dropna()

    print(df.shape)

    column_l = ['avg_rank_{0}'.format(cutoff) for cutoff in cutoff_l]

    n = len(column_l)

    fig = make_subplots(
        rows=n, cols=n, shared_xaxes=True, shared_yaxes=True, horizontal_spacing=0.005, vertical_spacing=0.005
    )

    for i in range(n):
        for j in range(i + 1):

            fig.add_trace(
                go.Scatter(
                    x=df[column_l[i]], y=df[column_l[j]], mode='markers', showlegend=False,
                    marker={
                        'color': colors['orange'] if association == 'atp' else colors['blue'],
                        'symbol': 'circle' if association == 'atp' else 'square'
                    }
                ),
                row=1 + i, col=1 + j
            )

            if i > j:

                x, y = df[column_l[i]], df[column_l[j]]
                slope, intercept = np.polyfit(x, y, 1)
                y_pred = slope * x + intercept
                ss_res = np.sum((y - y_pred) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r_squared = 1 - (ss_res / ss_tot)

                fig.add_trace(
                    go.Scatter(
                        x=df[column_l[i]], y=y_pred, mode='lines', showlegend=False,
                        line={'width': 0.5, 'color': colors['black']}
                    ),
                    row=1 + i, col=1 + j
                )
                fig.add_annotation(
                    x=12, y=0.5,
                    xanchor='left', yanchor='bottom',
                    text=r'r² = {0:.2f}'.format(r_squared),
                    showarrow=False,
                    row=1 + i, col=1 + j
                )

    width = 650
    height = 650
    fig.update_layout(
        width=width, height=height,
        title='{0} Top {1} by Average Rank (from Linear Extensions)'.format(association.upper(), plot_cutoff),
        margin=dict(l=10, r=10, b=20, t=30)
    )

    for i, cutoff in enumerate(cutoff_l):
        fig.update_xaxes(title_text='Cutoff {0}'.format(cutoff), row=4, col=1 + i, range=[0.05, plot_cutoff + 1])
        fig.update_yaxes(title_text='Cutoff {0}'.format(cutoff), row=1 + i, col=1, range=[0.05, plot_cutoff + 1])

    fig.write_image(
        './scatter/scatter_{0}-{1}-{2}.pdf'.format(version, association, plot_cutoff),
        width=width, height=height, scale=1
    )


if __name__ == '__main__':

    ver_l = ['nonadj']
    assc_l = ['wta', 'atp']
    ctff_l = [3, 5, 10, 20]
    plt_ctff_l = [25]

    for ver in ver_l:
        for assc in assc_l:
            for plt_ctff in plt_ctff_l:
                main(ver, assc, ctff_l, plt_ctff)


# cutoff = 5
#
# if association == 'atp':
#     decades = [
#         '70', '80', '90', '00', '10', '20'
#     ]
# elif association == 'wta':
#     decades = [
#         '80', '90', '00', '10', '20'
#     ]
# else:
#     raise Exception('Association {0} not supported!'.format(association))
#
# years = []
# for decade in decades:
#     for y in range(10):
#         if decade in {'00', '10', '20'}:
#             year = str(int('20' + decade) + y)
#         else:
#             year = str(int('19' + decade) + y)
#         if int(year) > 2023:
#             continue
#         years.append(year)
#
# files = [
#     './tennis_{0}/{1}_matches_{2}.csv'.format(association, association, year) for year in years
# ]
#
# matches_df = pd.concat([pd.read_csv(file, usecols=['tourney_level', 'winner_id', 'loser_id', 'round']) for file in files])
# matches_df = matches_df[matches_df['round'].isin(['F']) & matches_df['tourney_level'].isin(['G'])]
#
# # matches_df = pd.DataFrame({
# #     'player_id': pd.concat([matches_df['winner_id'], matches_df['loser_id']]).reset_index(drop=True)
# # })
#
# matches_df['player_id'] = matches_df['winner_id']
#
#
# players_file = './tennis_{0}/{1}_players.csv'.format(association, association)
# players_df = pd.read_csv(players_file, usecols=['player_id', 'name_first', 'name_last'])
# players_df['name'] = players_df['name_first'] + ' ' + players_df['name_last']
# players_df = players_df.drop(columns=['name_first', 'name_last'])
#
# df = pd.merge(matches_df, players_df, on='player_id')
#
# with open('./results/{0}_player_idx_to_id_{1}-{2}.pkl'.format('', association, cutoff), 'rb') as file:
#     player_idx_to_id = pickle.load(file)
# with open('./results/{0}_player_idx_to_name_{1}-{2}.pkl'.format('', association, cutoff), 'rb') as file:
#     player_idx_to_name = pickle.load(file)
# with open('./posets/{0}_out_{1}-{2}.pkl'.format('', association, cutoff), 'rb') as file:
#     g = pickle.load(file)
# dist = dict()
# for generation, nodes in enumerate(nx.topological_generations(g)):
#     for i in nodes:
#         dist[player_idx_to_name[i]] = generation
#
# df = df['name'].value_counts()
# df = df.reset_index()
# df.columns = ['name', 'count']
#
#
# dist_df = pd.DataFrame(dist.items(), columns=['name', 'dist'])
#
# df = pd.merge(df, dist_df, on='name')
#
#
# fig = px.scatter(df, x='dist', y='count', hover_data=['name'])
# fig.show()