import requests
import os
import datetime

API_ID = os.environ['API_ID_workout']
API_KEY = os.environ["API_KEY_nutritionix"]
USER_NAME = "anna"
SHEET_API_PASS = os.environ["SHEET_API_PASS"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["sheet_endpoint"]

question = input("Tell me which exercise you did:")

parameters = {
    "query": question,
    "gender": "female",
    "weight_kg": 72.5,
    "height_cm": 167.64,
    "age": 30
}

headers = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

req = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
req_json = req.json()

date = datetime.date.today().strftime('%d/%m/%Y')
time = datetime.datetime.now().strftime('%H:%M')

for i in req_json["exercises"]:
    sheet_puts = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": i["name"].title(),
            "duration": i['duration_min'],
            "calories": i['nf_calories']
        }
    }

sheet_res = requests.post(url=sheet_endpoint, json=sheet_puts, auth=(USER_NAME, SHEET_API_PASS))
print(sheet_res.text)
