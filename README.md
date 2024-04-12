# technical-task

The goal of this project was to convert raw GPS data into meaningful metrics that could be used by a coach. 

The code computes four key metrics based on the athlete's data:
* Total distance
* Distance at speed zone 5
* Top speed
* and time with the ball.

The user can then choose to rank the players based on any of these four metrics. 

## How to use the project: 

1. Clone the git repo.
2. Unzip the data file 'match_data.csv.zip' which is stored in the data folder. 
3. Run the main python script by running
```
python ./scripts/main.py
```
in the terminal.

4. Run the leaderboards script using 
```
python ./scripts/leaderboards.py
```
5. Once this script is running, you will be prompted to input the metric you wish the leaderboard to be ranked using. This can be any of 'Top Speed', 'Total Distance', 'Distance in Zone 5' or 'Time With Ball'.
6. The output will be a leaderboard of players ranked based on your chosen metric.

## Time spent on each section: 
* Discovery - approximately 1hr.
* Execution - approximately 5hrs.
* Presentation - approximately 2hrs. 
