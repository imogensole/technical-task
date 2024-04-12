import pandas as pd 

# Read in the data 
data = pd.read_csv("data/player_metrics.csv")

# Get the list of calculated metrics 
metrics = data.drop(columns=['participation_id']).columns

# Create leaderboard for each metric and save as a csv file 
for metric in metrics: 
    leaderboard = data.sort_values(by=metric, ascending=False)[['participation_id', metric]]
    leaderboard.to_csv(f"output/leaderboard_{metric.replace(' ', '_').lower()}.csv", index=False)

while True:
    # Ask user to choose a metric for the leaderboard 
    metric = input("How would you like the players ranked? Choose from 'Top Speed', 'Total Distance', 'Distance in Zone 5', 'Number of Sprint Events' or 'Time With Ball' ")

    if metric in data.columns:
        # Sort leaderboard based on the chosen metric 
        leaderboard = data.sort_values(by=metric, ascending=False)[['participation_id', metric]]

        print("Leaderboard based on", metric)
        print(leaderboard)
    else:
        # Show error message if chosen metric is invalid 
        print("Sorry, the entered metric is not valid.")

    # Ask user if they would like to view another leaderboard
    continues = input("Would you like to view another leaderboard? (yes/no)")

    if continues != 'yes': 
        break
