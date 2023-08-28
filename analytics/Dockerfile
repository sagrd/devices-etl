FROM python:3-slim
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2 sqlalchemy \
    && pip install pymysql cryptography pandas geopy
WORKDIR /app
COPY . .
CMD [ "python", "./analytics.py" ]