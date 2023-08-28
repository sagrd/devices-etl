EXTRACT_DATA_LAST_HOUR_QUERY = """
      select device_id,temperature,location,to_timestamp(time::int) as event_dt
      from devices
      where to_timestamp(time::int) between current_timestamp - interval '30 seconds' and current_timestamp"""