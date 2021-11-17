from skillcorner.client import SkillcornerClient

# Create client object
client = SkillcornerClient(username='PUT_YOUR_LOGIN_HERE', password='PUT_YOUR_PASSWORD_HERE')

# Get data from simple endpoint
data = client.get_competitions()
print(data)

# Get and save data from simple endpoint
client.get_and_save_competitions(filepath="competitions.json", params={'season': 5})

# Get data from endpoint using object id
data = client.get_match(match_id=49364)
print(data)

# Get and save data from endpoint using object id
client.get_and_save_match(match_id=49364, filepath='match.json')

# Usage of extra 'params' parameter
# Get physical data using 'params' parameter
data = client.get_physical(params={'season': 7, 'team': 4})
print(data)
client.get_and_save_physical(filepath="physical.json", params={'season': 8, 'team': 76})

data = client.get_matches(params={'season': 6, 'team': 327})
print(data)
client.get_and_save_matches(filepath="matches.json", params={'competition_edition': 171, 'date_time__gt': '2021-02-10'})

# Use all remaining methods
data = client.get_teams(params={'competition_edition': 141})
print(data)
client.get_and_save_teams(filepath="teams.json")

data = client.get_team(team_id=2)
print(data)
client.get_and_save_team(team_id=2, filepath="team.json")

data = client.get_players(params={'team': 481, 'competition_edition': 115})
print(data)
client.get_and_save_players(filepath="players.json", params={'team': 481, 'competition_edition': 115})

client.get_player(player_id=38759)
print(data)
client.get_and_save_player(player_id=38759, filepath="player.json")

data = client.get_competition_editions(competition_id=4)
print(data)
client.get_and_save_competition_editions(competition_id=4, filepath="competition_editions.json")

data = client.get_match_tracking_data(match_id=49364)
print(data)
data = client.get_match_video_tracking_data(match_id=63743, params={"frame__gt": 58500})
print(data)
data = client.get_match_data_collection(match_id=62100)
print(data)

client.get_and_save_match_tracking_data(match_id=49364, filepath="tracking_data.json")
client.get_and_save_match_video_tracking_data(match_id=63743, filepath="video_tracking_data.json",
                                              params={"frame__gt": 58500})
client.get_and_save_match_data_collection(match_id=62100, filepath="data_collection.json")
