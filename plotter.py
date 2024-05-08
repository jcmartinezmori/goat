import itertools as it
import networkx as nx
import numpy as np
import pandas as pd
import pickle
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
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

association = 'wta'
max_rank = 10
max_generation = 6

with open('./results/player_idx_to_id_{0}_{1}.pkl'.format(association, max_rank), 'rb') as file:
    player_idx_to_id = pickle.load(file)
with open('./results/player_idx_to_name_{0}_{1}.pkl'.format(association, max_rank), 'rb') as file:
    player_idx_to_name = pickle.load(file)
n = len(player_idx_to_id)
out = pd.read_csv('./results/out_{0}-{1}.csv'.format(association, max_rank))
# out = pd.read_pickle('./results/out_{0}-{1}.pkl'.format(association, max_rank))
# out = out.iloc[100000:]
# out = out.iloc[0::10]
# out = out.iloc[0::2]
# out = out.iloc[1::2]


# fig = px.box(out, points='suspectedoutliers')
# fig.update_layout(
#     xaxis_title='Player',
#     yaxis_title='Ranking',
#     yaxis_range=[0, 165]
# )
# fig.show()
# fig.write_html('./html/out_{0}-{1}.html'.format(association, max_rank))


if max_generation is None:
    max_generation = n
    label = ''
else:
    label = 'name'
mu = np.zeros((n, n))
for i in range(n):
    name = player_idx_to_name[i]
    for r in out[name] - 1:
        mu[i][r] += 1
mu = mu / mu.sum(axis=1)


g = nx.DiGraph()
g.add_nodes_from(range(n))
for i, j in it.permutations(range(n), r=2):
    if all(sum(mu[i][:r]) >= sum(mu[j][:r]) for r in range(n)):
        g.add_edge(i, j)
g = nx.transitive_reduction(g)
subgraph = set()
for generation, nodes in enumerate(nx.topological_generations(g)):
    if generation <= max_generation:
        subgraph = subgraph.union(nodes)
g = nx.subgraph(g, subgraph)
for generation, nodes in enumerate(nx.topological_generations(g)):
    for i in nodes:
        g.nodes[i]['generation'] = generation
        g.nodes[i]['name'] = player_idx_to_name[i]
        if label == 'name':
            g.nodes[i]['label'] = g.nodes[i]['name']
        else:
            g.nodes[i]['label'] = ''
max_generation = max(data['generation'] for _, data in g.nodes(data=True))
for _, data in g.nodes(data=True):
    data['generation'] = max_generation - data['generation']
pos = nx.multipartite_layout(g, align='vertical', subset_key='generation', scale=1)

# for generation, nodes in enumerate(nx.topological_generations(g)):
#     for i in nodes:
#         pos[i][1] += np.random.uniform(-0.05, 0.05)

x, y = zip(*[pos[i] for i in g.nodes()])
node_trace = go.Scatter(
    x=x,
    y=y,
    mode='markers+text',
    text=[data['label'] for _, data in g.nodes(data=True)],
    textposition='top center',
    textfont=dict(
        family="sans serif",
        size=16,
        color=colors['black']
    ),
    marker=dict(
        color=colors['skyblue'],
        size=10,
        line=dict(
            color=colors['black'],
            width=1
        )
    )
)

x = [node_pos for edge_pos in [[pos[i][0], pos[j][0], None] for i, j in g.edges()] for node_pos in edge_pos]
y = [node_pos for edge_pos in [[pos[i][1], pos[j][1], None] for i, j in g.edges()] for node_pos in edge_pos]
edge_trace = go.Scatter(
    x=x,
    y=y,
    mode='lines',
    opacity=1,
    line=dict(
        color=colors['black'],
        width=0.5
    )
)
fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        paper_bgcolor=colors['white'],
        plot_bgcolor=colors['white'],
        showlegend=False,
        hovermode="closest",
        margin=dict(b=0, l=0, r=0, t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)
fig.write_html('./html/three-poset_{0}-{1}.html'.format(association, max_rank))
fig.write_image('./pdf/poset_{0}-{1}.pdf'.format(association, max_rank), width=1200, height=800, scale=1)

fig.show()

