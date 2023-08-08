FROM python:3.9-slim

LABEL maintainer="Belendia Serda belendia@gmail.com"

# Create a non-root user
ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" flare \
    && useradd --no-create-home --no-log-init -u "${UID}" -g "${GID}" flare


RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1
ENV DOCKER_CONTAINER 1

COPY ./flare/requirements.txt .
RUN pip install -r requirements.txt

COPY ./flare /flare
WORKDIR /flare

RUN chmod +x /flare/entrypoint.sh

# Switch to the non-root user
USER flare

EXPOSE 8000

# CMD ["unicorn", "--workers=3", "config.wsgi:application", "0:8000", "--log-level debug"]
CMD ["./entrypoint.sh"]