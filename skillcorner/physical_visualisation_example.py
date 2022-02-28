from pandasgui import show
from skillcorner.client import SkillcornerClient


skc_client = SkillcornerClient(username='PUT_YOUR_LOGIN_HERE', password='PUT_YOUR_PASSWORD_HERE')
physical_data = skc_client.get_physical(params={'season': 6, 'competition': 1})
show(physical_data)
