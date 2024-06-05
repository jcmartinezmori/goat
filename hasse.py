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


def main(version, association, cutoff, plot_cutoff):

    with open('./posets/{0}_out_{1}-{2}.pkl'.format(version, association, cutoff), 'rb') as file:
        g = pickle.load(file)
    if plot_cutoff is None:
        plot_cutoff = g.number_of_nodes()

    subgraph = set()
    for dist, nodes in enumerate(nx.topological_generations(g)):
        if dist <= plot_cutoff:
            subgraph = subgraph.union(nodes)
    g = nx.subgraph(g, subgraph)
    max_dist = max(data['dist'] for _, data in g.nodes(data=True))
    for _, data in g.nodes(data=True):
        data['plot_dist'] = max_dist - data['dist']
        if plot_cutoff == g.number_of_nodes():
            data['label'] = ''
        else:
            data['label'] = data['player_name']
    pos = nx.multipartite_layout(g, align='vertical', subset_key='plot_dist', scale=1)

    node_x, node_y = zip(*[pos[i] for i in g.nodes()])
    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=[data['label'] for _, data in g.nodes(data=True)],
        textposition='top center',
        textfont=dict(
            # family="sans serif",
            size=12,
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

    edge_x = [node_pos for edge_pos in [[pos[i][0], pos[j][0], None] for i, j in g.edges()] for node_pos in edge_pos]
    edge_y = [node_pos for edge_pos in [[pos[i][1], pos[j][1], None] for i, j in g.edges()] for node_pos in edge_pos]
    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        opacity=0.5,
        line=dict(
            color=colors['black'],
            width=0.25
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

    fig.write_image(
        './pdf/hasse_{0}-{1}-{2}.pdf'.format(association, cutoff, plot_cutoff),
        width=1200, height=325, scale=1
    )


if __name__ == '__main__':

    ver = ''
    association_l = ['atp', 'wta']
    cutoff_l = [3, 5, 10, 20]
    plot_cutoff_l = [6, None]

    for assc in association_l:
        for ctff in cutoff_l:
            for plt_ctff in plot_cutoff_l:
                main(ver, assc, ctff, plt_ctff)
