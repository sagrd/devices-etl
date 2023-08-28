Devices ETL
- 

## Running the docker:
- To get started run `docker-compose up` in root directory.
- It will create the PostgresSQL database and start generating the data.
- It will create an empty MySQL database.
- It will launch the analytics.py script which will perform necessary transformation and load the data in mysql format.


## Observations and improvements
- `platform: linux/x86_64` added in mysql_db in `docker-compose.yml` to run the container in mac. The updated script should work on all unix based environments.

### Design:
- Scheduling from code is not the best way to run the tasks at interval (see Quality Issues). One way of solving the problem scheduling is to run cronjob from `analytics` container. The container would stop after running the job once so we will need to find a way to keep the container running in the background. Even better way to achive this is by ocrastating the job via the `main` container - as the container wont be stopped because of `async loop` running forever (see `main.py`).


### Quality Issues:
- When scheduling with `sleep()` or with any `current_time` based approach , there could be issue with completeness of the data given the events on `devices` table are generated every miliseconds. This design may not account for the time required for transformation (and running code) which can cause data incompleteness. There are few ways to tackle this.
1. When pulling the data, consider `max(extract_dt)` from `mysql table`. And pull everything after the resulatant timestamp. This should work as the `extract_dt` column is actually timestamp for latest row for `devices` data but not creation datetime of the row on `devices` table on `mysql`
2. If 1 hr delay is acceptable, it might be a good idea to generate rows for `analytics` table grouping on `date and hour` fields of `devices` table. This should solve above mentioned issues and perhaps will be more intuitive in terms of interpreting results.

