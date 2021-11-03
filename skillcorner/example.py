from skillcorner.client import SkillcornerClient

# Create client object
client = SkillcornerClient(username='', password='')

# Get data from simple endpoint

# Get data from endpoint using object id
data = client.get_match(match_id=49364)
print(data)

# Get and save data from simple endpoint

# Get and save data from endpoint using object id
client.get_and_save_match(match_id=49364, filepath='match.json')

# Usage of extra 'params' parameter
# Get physical data using 'params' parameter
data = client.get_physical(params={'season': 8, 'team': 1415})
print(data)
client.get_and_save_physical(filepath="physical.json", params={'season': 6, 'team': 1415})

# Use all remaining methods
data = client.get_teams()
print(data['count'])
client.get_and_save_teams(filepath="teams.json")

data = client.get_team(team_id=2)
print(data)
client.get_and_save_team(team_id=2, filepath="team.json")

data = client.get_players()
print(data['count'])
client.get_and_save_players(filepath="players.json")

client.get_player(player_id=38759)
print(data)
client.get_and_save_player(player_id=38759, filepath="player.json")

data = client.get_competitions()
print(data['count'])
client.get_and_save_competitions(filepath="competitions.json")

data = client.get_competition_editions(competition_id=4)
print(data['count'])
client.get_and_save_competition_editions(competition_id=4, filepath="competition_editions.json")

data = client.get_match_tracking_data(match_id=49364)
print(data)
data = client.get_match_video_tracking_data(match_id=49364)
print(data)
data = client.get_match_data_collection(match_id=49364)
print(data)

client.get_and_save_match_tracking_data(match_id=49364, filepath="tracking_data.json")
client.get_and_save_match_video_tracking_data(match_id=49364, filepath="video_tracking_data.json")
client.get_and_save_match_data_collection(match_id=49364, filepath="data_collection.json")
