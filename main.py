import requests
import re
import yaml
import pandas as pd
import urllib3

with open('./conf/conf.yaml') as f:
    conf = yaml.safe_load(f)
print(conf)

CLIENT_ID=conf['client_id']
CLIENT_SECRET=conf['client_secret']
REFRESH_TOKEN=conf['client_token']

access_token = "access_token=" + REFRESH_TOKEN # enter your access code here
url = "https://www.strava.com/api/v3/activities"

page = 1

while True:
    
    # get page of activities from Strava
    r = requests.get(url + '?' + access_token + '&per_page=50' + '&page=' + str(page))
    r = r.json()
    print(r)

    # if no results then exit loop
    if (not r):
        break
    
    # otherwise add new data to dataframe
    for x in range(len(r)):
        activities.loc[x + (page-1)*50,'id'] = r[x]['id']
        activities.loc[x + (page-1)*50,'type'] = r[x]['type']

    # increment page
    page += 1

# barchart of activity types
activities.head()
activities['type'].value_counts().plot('bar')
plt.title('Activity Breakdown', fontsize=18, fontweight="bold")
plt.xticks(fontsize=14)
plt.yticks(fontsize=16)
plt.ylabel('Frequency', fontsize=18)
 
# filter to only runs
runs = activities[activities.type == 'Run']

# initialize dataframe for split data
col_names = ['average_speed','distance','elapsed_time','elevation_difference','moving_time','pace_zone',
             'split','id','date','description']
splits = pd.DataFrame(columns=col_names)

# loop through each activity id and retrieve data
for run_id in runs['id']:
    
    # Load activity data
    print(run_id)
    r = requests.get(url + '/' + str(run_id) + '?' + access_token)
    r = r.json()

    # Extract Activity Splits
    activity_splits = pd.DataFrame(r['splits_metric']) 
    activity_splits['id'] = run_id
    activity_splits['date'] = r['start_date']
    activity_splits['description'] = r['description']
    
    # Add to total list of splits
    splits = pd.concat([splits, activity_splits])