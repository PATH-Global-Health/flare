FROM python:3.7

LABEL maintainer="Belendia Serda belendia@gmail.com"

RUN apt-get -q update && apt-get -qy install netcat

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

COPY . /code/
WORKDIR /code/
RUN mv wait-for /bin/wait-for

EXPOSE 8000

RUN adduser --disabled-password --gecos '' webuser

CMD ["gunicorn", "flare.wsgi", "0:8000"]