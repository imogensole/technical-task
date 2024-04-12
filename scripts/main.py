import pandas as pd
import numpy as np

# Read in the data 
data = pd.read_csv("data/match_data.csv")

# Filter and sort the data 
data_filtered = data[(data['Pitch_x'] >= -52.5) & (data['Pitch_x'] <= 52.5) 
                     & (data['Pitch_y'] >= -34) & (data['Pitch_y'] <= 34)]
data_sorted = data_filtered.sort_values(by='Time (s)')

# Separate data for players and ball
all_players_data = data_sorted[data_sorted['participation_id'] != 'ball']
ball_data = data_sorted[data_sorted['participation_id'] == 'ball']

# function to smooth noise in speed measurements 
def smooth_speed(player_data):
    player_data['Speed (m/s)'] = player_data['Speed (m/s)'].rolling(window=3).mean()
    return player_data

# Applying the function grouped by 'participation_id'
smooth_speeds = all_players_data.groupby('participation_id').apply(smooth_speed)

# Convert the index back to regular columns
smooth_speeds = smooth_speeds.reset_index(level=0, drop=True)


def total_distance(player_data):
    '''
    Takes the GPS data for a single player and computes the total distance 
    travelled during play. 
    '''

    # Get differences between subsequent positions 
    x_diff = player_data['Pitch_x'].diff()
    y_diff = player_data['Pitch_y'].diff()

    # Calculate the distance between subsequent positions
    distances = np.sqrt(x_diff**2 + y_diff**2)

    # Sum distances 
    total_dist = np.sum(distances)

    return total_dist


def total_dist_zone5(player_data):
    '''
    Takes the GPS data for a single player and computes the total distance travelled in speed 
    zone 5. 
    '''

    # Get differences between subsequent positions 
    x_diff = player_data['Pitch_x'].diff()
    y_diff = player_data['Pitch_y'].diff()

    # Calculate distances between subsequent positions 
    distances = np.sqrt(x_diff**2 + y_diff**2)

    # Create a mask to get distances while in zone 5 
    mask = (player_data['Speed (m/s)'] <= 7.03) &  (player_data['Speed (m/s)'] >= 5.5)
    distances_selected = distances[mask]

    # Sum distances in zone 5 
    total_z5 = np.sum(distances_selected)

    return total_z5

# Define function to calculate time player has possession of ball
def calc_time_with_ball(player_data, ball_data):
    '''
    Takes the GPS data for a single player and computes the total time the player is less than 3m from the 
    ball. 
    '''
    # Get times and positions of player and ball 
    player_positions = player_data[['Time (s)', 'Pitch_x', 'Pitch_y']]
    ball_positions = ball_data[['Time (s)', 'Pitch_x', 'Pitch_y']]

    # Find the common times between the player and the ball
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

def count_sprints(player_data):
    # Create a mask to get distances while in zone 5 
    mask = (player_data['Speed (m/s)'] <= 7.03) &  (player_data['Speed (m/s)'] >= 5.5)

    # Find continuous sections where the mask is True 
    mask_diff = np.concatenate(([0], np.diff(mask.astype(int)), [0]))

    # Find indices of starts and ends of sprints 
    sprint_starts_idx = np.where(mask_diff == 1)
    sprint_ends_idx = np.where(mask_diff == -1)

    # Get start and end times of sprints 
    start_times = np.array(player_data['Time (s)'].iloc[sprint_starts_idx])
    end_times = np.array(player_data['Time (s)'].iloc[sprint_ends_idx])

    # Calculate length of each sprint 
    sprint_lengths = end_times - start_times

    # Count total number of sprints longer than 2s 
    total_sprints = sum(sprint_lengths > 2)
    
    return total_sprints


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

# Apply time with ball function
number_sprints = all_players_data.groupby('participation_id').apply(count_sprints)
number_sprints.name = 'Number of Sprint Events'

# Combine metrics into a single DataFrame
combined_data = top_speeds.join(total_distances).join(total_distances_z5).join(time_with_ball).join(number_sprints)

# Write to a csv
combined_data.to_csv('data/player_metrics.csv')

