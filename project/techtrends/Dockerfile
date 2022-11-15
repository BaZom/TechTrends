FROM python:3.8
LABEL maintainer="Basem Abughallya"

COPY TechTrends/project/techtrends /usr/src/app
WORKDIR /usr/src/app

RUN pip install  --no-cache-dir -r requirements.txt
RUN python init_db.py

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
