from datetime import datetime, timedelta

import pandas as pd
import pytz
import sqlalchemy
from apify_client import ApifyClient
from trycourier import Courier


engine = sqlalchemy.create_engine('sqlite:///instance/data.db')

# read table from database
database = pd.read_sql_table('user', engine)

# get today's date in Canada/Eastern timezone
timezone = pytz.timezone('UTC')
date_today = datetime.now(timezone)
date_yesterday = datetime.strptime('2022-11-03', '%Y-%m-%d')


def get_info(province_, city_, fuel_):
    # Initialize the ApifyClient with your API token
    client = ApifyClient("apify_api_7DKpNJdyHyY2a2rihOxwBSyG6Achjn3Wbj9u")

    run_input = {
        "location": str(city_ + ', ' + province_),
        "maxCrawledPlacesPerSearch": 3,
    }

    # Run the API for getting das prices
    run = client.actor("natasha.lekh/gas-prices-scraper").call(run_input=run_input)

    if fuel_ == 'Regular gas':
        fuel_ = 'Regular'
    elif fuel_ == 'Premium gas':
        fuel_ = 'Premium'
    elif fuel_ == 'Diesel':
        fuel_ = 'Diesel'

    information_for_mail = []
    # Adding information about gas station and price to list
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        for k in range(len(item['gasPrices'])):
            if item['gasPrices'][k]['gasType'] == fuel_:
                fuel_index = k
                information_for_mail.append((item['title'], item['gasPrices'][fuel_index]['priceTag'],
                                             item['gasPrices'][fuel_index]['gasType'], item['street']))
            else:
                continue

    sorted_information = sorted(information_for_mail, key=lambda x: x[1])
    info = str()
    for si in sorted_information[:5]:
        si = ' '.join(si)
        info += (si + '\n')
    return info


# Sending notification by mail
def send_mail(name_, email_, information_):
    client = Courier(auth_token="pk_prod_G824KWJR0D4YTBJ1BR61893JYX8S")

    resp = client.send_message(
      message={
        "to": {
          "email": email_
        },
        "content": {
          "title": "Welcome to Courier Reminder about Gas prices!",
          "body": f"Hello, {name_}! \n {{info}}"
        },
        "data": {
          "info": information_
        },
      }
    )
    return resp['requestId']


# Iterate over DataFrame rows
while date_today.date() != date_yesterday.date():
    for i, row in database.iterrows():
        next_date = row['next_date']
        user_freq = row['frequency']

        if str(next_date)[:10] == str(date_today.date()):
            if send_mail(name_=row['name'], email_=row['email'], information_=get_info(province_=row['province'],
                         city_=row['city'], fuel_=row['type_of_fuel'])):
                if user_freq == 'Every day':
                    next_date = (date_today + timedelta(days=1)).date()
                elif user_freq == 'Once a week':
                    next_date = (date_today + timedelta(weeks=1)).date()
                elif user_freq == 'Twice a month':
                    next_date = (date_today + timedelta(weeks=2)).date()
                elif user_freq == 'Once a month':
                    next_date = (date_today + timedelta(weeks=4)).date()

                # Update the row in the database
                database.at[i, 'next_date'] = next_date
                # write the updated table back to the database
                database.to_sql('user', engine, if_exists='replace', index=False)

    date_yesterday = date_today
