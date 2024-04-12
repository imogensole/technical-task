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

def count_sprints(player_data):
    # Create a mask to get distances while in zone 5 
    mask = (player_data['Speed (m/s)'] <= 7.03) &  (player_data['Speed (m/s)'] >= 5.5)
    
    time_diff = np.diff(player_data['Time (s)'])

    # Find continuous sections where the mask is True 
    mask.diff = np.concatenate(([0], np.diff(mask.astype(int)), [0]))

    return mask.diff

count_sprints(ball_data)
    
