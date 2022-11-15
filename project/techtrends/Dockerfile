FROM python:3.8
LABEL maintainer="Basem Abughallya"

WORKDIR /usr/src/app
COPY ./requirements.txt ./
COPY . ./
RUN python init_db.py
RUN pip install -r requirements.txt
EXPOSE 3111
CMD [ "python", "app.py" ]
