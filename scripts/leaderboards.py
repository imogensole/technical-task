import pandas as pd 

# Read in the data 
data = pd.read_csv("data/player_metrics.csv")

while True:
    metric = input("How would you like the players ranked? Choose from 'Top Speed', 'Total Distance', 'Distance in Zone 5' or 'Time With Ball' ")

    if metric in data.columns:
        leaderboard = data.sort_values(by=metric, ascending=False)[['participation_id', metric]]

        print("Leaderboard based on", metric)
        print(leaderboard)
    else:
        print("Sorry, the entered metric is not valid.")

    continues = input("Would you like to view another leaderboard? (yes/no)")

    if continues != 'yes': 
        break