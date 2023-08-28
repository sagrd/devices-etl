Devices ETL
- 

## Running the docker:
- To get started run `docker-compose up` in root directory.
- It will create the PostgresSQL database and start generating the data.
- It will create an empty MySQL database.
- It will launch the analytics.py script which will perform necessary transformation and load the data in mysql format.


## Notes:
- `platform: linux/x86_64` added in mysql_db in `docker-compose.yml` to run the container in mac. The updated script should work on all unix based environments.

