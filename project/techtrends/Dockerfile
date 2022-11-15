FROM python:3.8
LABEL maintainer="Basem Abughallya"

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY . ./
RUN python init_db.py
EXPOSE 3111
CMD [ "python", "app.py" ]
