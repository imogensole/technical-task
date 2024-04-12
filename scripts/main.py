import pandas as pd
import numpy as np

# Read in the data 
data = pd.read_csv("data/match_data.csv")

# Filter and sort the data 
data_filtered = data[(data['Pitch_x'] >= -52.5) & (data['Pitch_x'] <= 52.5) & (data['Pitch_y'] >= -34) & (data['Pitch_y'] <= 34)]
all_players_data = data_filtered[data_filtered['participation_id'] != 'ball']
all_players_data = all_players_data.sort_values(by='Time (s)')
ball_data = data_filtered[data_filtered['participation_id'] == 'ball']

# Define function to calculate the total distance 
def total_distance(player_data):

    # Get differences between subsequent positions 
    x_diff = player_data['Pitch_x'].diff()
    y_diff = player_data['Pitch_y'].diff()

    # Calculate distance between subsequent positions
    distances = np.sqrt(x_diff**2 + y_diff**2)

    # Sum distances 
    total_dist = np.sum(distances)

    return total_dist


# Define function to calculate the total distance in zone 5 
def total_dist_zone5(player_data):

    # Get differences between subsequent positions 
    x_diff = player_data['Pitch_x'].diff()
    y_diff = player_data['Pitch_y'].diff()

    # Calculate distances between subsequent positions 
    distances = np.sqrt(x_diff**2 + y_diff**2)

    # Create mask to get distances while in zone 5 
    mask = (player_data['Speed (m/s)'] <= 7.03) &  (player_data['Speed (m/s)'] >= 5.5)
    distances_selected = distances[mask]

    # Sum distances in zone 5 
    total_z5 = np.sum(distances_selected)

    return total_z5

# Define function to calculate time player has possession of ball
def calc_time_with_ball(player_data, ball_data):

    # Get times and positions of player and ball 
    player_positions = player_data[['Time (s)', 'Pitch_x', 'Pitch_y']]
    ball_positions = ball_data[['Time (s)', 'Pitch_x', 'Pitch_y']]

    # Find the common times between player and ball
    common_times = np.intersect1d(player_positions['Time (s)'], ball_positions['Time (s)'])

    # Filter player and ball positions to only include common times
    player_positions_common = player_positions[player_positions['Time (s)'].isin(common_times)][['Pitch_x', 'Pitch_y']].values
    ball_positions_common = ball_positions[ball_positions['Time (s)'].isin(common_times)][['Pitch_x', 'Pitch_y']].values

    # Calculate distances between player and ball at common time points
    distances = np.linalg.norm(ball_positions_common - player_positions_common, axis=1)

    # Calculate time with ball less than or equal to 3m away
    time_diff = np.diff(common_times)
    time_with_ball = np.sum(np.where((distances[:-1] <= 3) & (time_diff > 0), time_diff, 0))

    return time_with_ball

# Calculate the top speeds 
speeds = all_players_data[['participation_id', 'Speed (m/s)']]
top_speeds = speeds.groupby('participation_id').max()
top_speeds = top_speeds.rename(columns={'Speed (m/s)': 'Top Speed'})

# Apply total distance function
total_distances = all_players_data.groupby('participation_id').apply(total_distance)
total_distances.name = 'Total Distance'

# Apply distance is z5 function
total_distances_z5 = all_players_data.groupby('participation_id').apply(total_dist_zone5)
total_distances_z5.name = 'Distance in Zone 5'

# Apply time with ball function
time_with_ball = all_players_data.groupby('participation_id').apply(calc_time_with_ball, ball_data=ball_data)
time_with_ball.name = 'Time With Ball'

# Combine metrics into a single DataFrame
combined_data = top_speeds.join(total_distances).join(total_distances_z5).join(time_with_ball)

# Write to a csv
combined_data.to_csv('data/player_metrics.csv')

