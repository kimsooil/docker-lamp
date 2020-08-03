import requests
import sys
import time
from copy import deepcopy
from datetime import datetime

# python precomputes.py username[1] password[2] state_name[3] base_api_url[4] client_id[5] client_secret[6]
BASE_API_URL = sys.argv[4]
URL = BASE_API_URL+'covid/api/simulations/'
TOKEN = 'users/api/token/'
STATE_COUNTIES = 'model/api/v1/get_states_counties/'
META = 'meta/'
# with 9 minute average per run, at most 108 tasks will be running per state
# AWS FARGATE SPOT max is 250 tasks
SLEEP_TIME = 2
# client id and secret should be moved?
token_payload = {
    "username": sys.argv[1],
    "password": sys.argv[2],
    "client_id": sys.argv[5],
    "client_secret": sys.argv[6],
    "grant_type": "password"
}
# get token
try:
    r = requests.post(
        BASE_API_URL+TOKEN, json=token_payload)
    r.raise_for_status()
except:
    print("error attempting to get token")

headers = {"Authorization": "Bearer " + str(r.json().get("access_token"))}
state_name = sys.argv[3]
# get counties
try:
    r = requests.get(BASE_API_URL+STATE_COUNTIES, headers=headers)
    r.raise_for_status()
except:
    print("error gettingcounties")

counties = r.json()["counties"].get(state_name)
default_input = {
    "state": state_name,
    "county": []
}
# get default input
try:
    r = requests.get(BASE_API_URL+META)
    r.raise_for_status()
except:
    print("Error getting model defualts")

default_input.update({"country": r.json().get("country")})
default_input.update({"nDraws": str(r.json().get("model_defaults")["nDraws"])})
default_input.update(
    {"sim_length": str(r.json().get("model_defaults")["sim_length"])})
states = r.json().get("states")
default_counties = []

for state in states:
    if state.get("name") == state_name:
        default_input.update({"shelter_date": state.get("shelter_date")})
        default_input.update(
            {"shelter_release_start_date": state.get("shelter_release_start_date")})
        default_input.update(
            {"shelter_release_end_date": state.get("shelter_release_end_date")})
        default_input.update(
            {"social_distancing": state.get("social_distancing")})
        default_input.update(
            {"social_distancing_end_date": state.get("social_distancing_end_date")})
        default_input.update(
            {"quarantine_percent": state.get("quarantine_percent")})
        default_input.update(
            {"quarantine_start_date": state.get("quarantine_start_date")})
        default_counties = state.get("default_counties")

default_input["social_distancing"]
county_defaults = deepcopy(default_input)
payload = {"model_input": default_input}

# run models
print("\n--- DEFAULT COUNTIES ---")
payload["model_input"]["county"] = default_counties
quarantine_percent = 0

while quarantine_percent < 100:
    payload["model_input"]["quarantine_percent"] = quarantine_percent
    payload["model_input"]["social_distancing"] = True
    r = requests.post(URL, headers=headers, json=payload)
    print(payload['model_input']['county'], r.status_code)
    if r.status_code == 201:
        time.sleep(SLEEP_TIME)
    payload["model_input"]["social_distancing"] = False
    r = requests.post(URL, headers=headers, json=payload)
    print(payload['model_input']['county'], r.status_code)
    if r.status_code == 201:
        time.sleep(SLEEP_TIME)
    quarantine_percent += 25

print("\n--- ALL COUNTIES - DEFAULT PARAMATERS ---")
payload = {"model_input": county_defaults}

for county in counties:
    payload["model_input"]["county"] = [county]
    r = requests.post(URL, headers=headers, json=payload)
    print(payload['model_input']['county'], r.status_code)
    if r.status_code == 201:
        time.sleep(SLEEP_TIME)
