import pandas as pd
import plotly.graph_objects as go

association = 'wta'
max_rank = 10

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

df = df[df['rank'] <= max_rank]

# Plotting
fig = go.Figure()

for name, group in df.groupby('name'):
    cumulative_counts = group['rank'].value_counts().sort_index().cumsum()
    if 1 not in cumulative_counts:
        continue
    if cumulative_counts[1] < 20:
        continue
    fig.add_trace(go.Scatter(x=cumulative_counts.index, y=cumulative_counts, mode='lines', name=name))

fig.update_layout(
    title='Cumulative Frequency Plot of Rank by Name',
    xaxis=dict(title='Rank'),
    yaxis=dict(title='Cumulative Frequency'),
    legend=dict(
        title='Name'
    )
)

fig.show()
