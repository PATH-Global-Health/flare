FROM python:3.9

LABEL maintainer="Belendia Serda belendia@gmail.com"

RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

COPY ./flare/requirements.txt .

RUN pip install pip --upgrade
RUN pip install -r requirements.txt

COPY ./flare /flare
# COPY .env /flare
# COPY wait-for .
# RUN mv wait-for /bin/wait-for
WORKDIR /flare

RUN chmod +x entrypoint.sh

EXPOSE 8000

# CMD ["unicorn", "--workers=3", "config.wsgi:application", "0:8000", "--log-level debug"]g
CMD ["./entrypoint.sh"]