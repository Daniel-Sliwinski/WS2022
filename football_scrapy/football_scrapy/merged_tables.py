#This code merges 
import pandas as pd

teams_df = pd.read_csv("teams.csv")

team_tables_df = pd.read_csv("team_table.csv")

full_team_df = pd.merge(teams_df, team_tables_df, left_on = ['season','team'], right_on=['season','team'], copy = False)
print(full_team_df)