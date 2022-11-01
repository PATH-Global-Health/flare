FROM python:3.9

LABEL maintainer="Belendia Serda belendia@gmail.com"

RUN apt-get -q update && apt-get -qy install netcat

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY . /code
#ADD ./flare_backend/requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

WORKDIR /code/
RUN mv wait-for /bin/wait-for

EXPOSE 8000

RUN adduser --disabled-password --gecos '' webuser

CMD ["gunicorn", "--workers=3", "flare.wsgi", "0:8000"]