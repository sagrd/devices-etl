from os import environ
from time import sleep
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, BigInteger, DateTime
from sqlalchemy.exc import OperationalError
from sql_queries import EXTRACT_DATA_LAST_HOUR_QUERY
from datetime import datetime
import json
from geopy import distance

def calculate_distance(location1, location2):
    '''calculates the distance between two location represented in (latitude, longitude) 
    args:
        - location1, location1: string (a dictionary) which can be converted to dict by json.loads()
    returns:
        - km: resultant value in km
    '''
    location1 = json.loads(location1)
    location2 = json.loads(location2)
    location1=(float(location1['latitude']),float(location1['longitude']))
    location2=(float(location2['latitude']),float(location2['longitude']))
    km = distance.distance(location1, location2).km
    return km


def transform_load_data_last_hour(psql_engine, mysql_engine):
    '''transforms the extracted data from postgresql
    args:
        - psql_engine, mysql_engine: sqlalchemy create_engine() for psql and mysql db
    returns:
        - None
    '''
    extracted_data = pd.read_sql(EXTRACT_DATA_LAST_HOUR_QUERY,psql_engine)
    print(extracted_data.columns)
    extracted_data = extracted_data.sort_values(['device_id','event_dt'], ascending = True)

    # the last location lead column will be empty
    extracted_data['location_lead'] = extracted_data.groupby(['device_id'])['location'].shift(-1).fillna(extracted_data['location'])
    extracted_data['distance'] = extracted_data.apply(lambda x: calculate_distance(x.location, x.location_lead), axis=1)
    transformed_data = extracted_data.groupby('device_id').agg(
                            {'temperature':'max',
                             'event_dt':['count','max'],
                             'distance':'sum'}).reset_index()
    transformed_data.columns = ['device_id','max_temperature','count_data_points','extract_dt','total_distance_km']
    transformed_data.to_sql('devices_agg_data', mysql_engine,if_exists='append', index = False)
    print("[INFO] Data Successfully Loaded to MySQL")


print('Waiting for the data generator...')
sleep(20)
print('ETL Starting...')

while True:
    try:
        psql_engine = create_engine(environ["POSTGRESQL_CS"], pool_pre_ping=True, pool_size=10)
        mysql_engine = create_engine(environ["MYSQL_CS"], pool_pre_ping=True, pool_size=10)
        metadata_obj = MetaData()
        devices_agg_data = Table(
            'devices_agg_data', metadata_obj,
            Column('device_id', String(50)),
            Column('max_temperature', Integer),
            Column('count_data_points', Integer),
            Column('total_distance_km', BigInteger),
            Column('extract_dt', DateTime),
        )
        metadata_obj.create_all(mysql_engine)
        break
    except OperationalError:
        sleep(0.1)
print('Connection to Databases Successful.')

transform_load_data_last_hour(psql_engine,mysql_engine)