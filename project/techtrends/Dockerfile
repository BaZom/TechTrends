FROM python:3.8
LABEL maintainer="Basem Abughallya"

WORKDIR /usr/src/app

COPY . ./

RUN pip install -r requirements.txt
RUN python init_db.py

EXPOSE 3111

CMD [ "python", "app.py" ]
