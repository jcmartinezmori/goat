import sage.all as sage
import pandas as pd
import pickle
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "browser"
import plotly.express as px

version = ''
association_l = ['atp', 'wta']
cutoff_l = [3, 5, 10, 20]
plot_cutoff_l = [25]

no_samples = 100000
for association in association_l:
    for cutoff in cutoff_l:
        for plot_cutoff in plot_cutoff_l:

            with open('./posets/{0}_out_{1}-{2}.pkl'.format(version, association, cutoff), 'rb') as file:
                g = pickle.load(file)

            data = (list(g.nodes()), list(g.edges()))
            p = sage.Poset(data, cover_relations=True)

            data = []
            for _, data in g.nodes(data=True):
                data['avg_rank'] = 0
            for _ in range(no_samples):
                ext = p.random_linear_extension()
                for r, i in enumerate(ext):
                    g.nodes[i]['avg_rank'] += (1 + r)

            data = [
                (idx, data['player_name'], data['player_id'], data['avg_rank'] / no_samples)
                for idx, data in g.nodes(data=True)
            ]

            df = pd.DataFrame(data, columns=['i', 'player_name', 'player_id', 'avg_rank'])
            df = df.sort_values(by='avg_rank')

            df.to_csv('./extensions/{0}_out_{1}-{2}.csv'.format(version, association, cutoff), index=False)

            df = df[:plot_cutoff]

            fig = px.line(df, x='player_name', y='avg_rank', markers=True)
            fig.update_layout(
                xaxis_title='',
                yaxis_title='Sample Average Rank (from Linear Extensions)',
                yaxis_range=[0, plot_cutoff + 2],
                margin=dict(b=10, l=10, r=10, t=10),
            )

            fig.write_image(
                './pdf/avg_rank_{0}-{1}-{2}.pdf'.format(association, cutoff, plot_cutoff),
                width=1200, height=480, scale=1
            )

