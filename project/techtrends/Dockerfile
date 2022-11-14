FROM python:3.8
LABEL maintainer="Basem Abughallya"

WORKDIR /usr/src/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN python init_db.py

EXPOSE 3111

CMD [ "python", "app.py" ]
