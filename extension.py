import sage.all as sage
import pandas as pd
import pickle
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


def main(version, association, cutoff, plot_cutoff, no_samples, load):

    if not load:

        with open('./poset/poset_{0}-{1}-{2}.pkl'.format(version, association, cutoff), 'rb') as file:
            g = pickle.load(file)
        p = sage.Poset((list(g.nodes()), list(g.edges())), cover_relations=True)

        for _, data in g.nodes(data=True):
            data['avg_rank'] = 0
        for _ in range(no_samples):
            ext = p.random_linear_extension()
            for r, i in enumerate(ext):
                g.nodes[i]['avg_rank'] += (1 + r)
        for _, data in g.nodes(data=True):
            data['avg_rank'] /= no_samples

        data = [
            (idx, data['player_name'], data['player_id'], data['avg_rank'])
            for idx, data in g.nodes(data=True)
        ]

        df = pd.DataFrame(data, columns=['i', 'player_name', 'player_id', 'avg_rank'])
        df = df.sort_values(by='avg_rank')
        df.to_csv('./extension/extension_{0}-{1}-{2}.csv'.format(version, association, cutoff), index=False)

    else:

        df = pd.read_csv('./extension/extension_{0}-{1}-{2}.csv'.format(version, association, cutoff))

    if plot_cutoff is None:
        plot_cutoff = df.shape[0]
    df = df[:plot_cutoff]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['player_name'],
        y=df['avg_rank'],
        mode='markers+lines',
        marker=dict(
            color=colors['orange'] if association == 'atp' else colors['blue'],
            symbol='circle' if association == 'atp' else 'square'
        ),
    ))
    fig.update_layout(
        xaxis_title='',
        yaxis_title='Average Rank',
        yaxis_range=[0, plot_cutoff + 2],
        margin=dict(b=10, l=10, r=10, t=10),
    )

    fig.write_image(
        './avg_rank/avg_rank_{0}-{1}-{2}-{3}.pdf'.format(version, association, cutoff, plot_cutoff),
        width=1200, height=325, scale=1
    )


if __name__ == '__main__':

    ver_l = ['nonadj']
    assc_l = ['wta', 'atp']
    ctff_l = [3, 5, 10, 20]
    plt_ctff_l = [20]
    no_sam = 100000
    ld = False

    for ver in ver_l:
        for assc in assc_l:
            for ctff in ctff_l:
                for plt_ctff in plt_ctff_l:
                    main(ver, assc, ctff, plt_ctff, no_sam, ld)
