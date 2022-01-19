"""
API CONFIGURABLES
"""
from jira import JIRA

# Insert your API credentials here
api_key = ""
user = ""
options = {"server": "http://server-name.com"}
jira_client = JIRA(options, basic_auth=(user, api_key))