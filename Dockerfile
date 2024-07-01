FROM python:3

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./datosaws /app

WORKDIR /app
RUN python manage.py collectstatic --noinput

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]