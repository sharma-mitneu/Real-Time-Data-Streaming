from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airmaster',
    'start_date': datetime(2024, 8, 3, 10)
}

def get_data():
    import requests

    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]


def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['picture'] = res['picture']['medium']

    # data we need to get from res -->
    # gender, address --> {street number, street name, city, state, country}, postcode, email, username, dob,
    # registered_date, phone


def stream_data():
    import json

    print(json.dumps(res, indent=3))

with DAG('user_automation',
         default_args = default_args,

         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )

stream_data()