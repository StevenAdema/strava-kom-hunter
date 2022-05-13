import requests
import re
import yaml
import pandas as pd
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open('./conf/conf.yaml') as f:
    conf = yaml.safe_load(f)
print(conf)

CLIENT_ID=conf['client_id']
CLIENT_SECRET=conf['client_secret']
REFRESH_TOKEN=conf['refresh_token']

auth_url = "https://www.strava.com/oauth/token"
# activites_url = "https://www.strava.com/api/v3/athlete/activities"
activites_url = "https://www.strava.com/api/v3//segments/explore"

payload = {
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'refresh_token': REFRESH_TOKEN,
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
# param = {'per_page': 200, 'page': 1}
param = {
    'bounds': '45.40576,-75.71238,45.42703,-75.67685',
    'activity_type': 'riding'
    }

my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset)
exit()
print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])