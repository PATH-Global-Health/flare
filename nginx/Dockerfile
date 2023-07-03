FROM nginx:latest-alpine
LABEL maintainer="Belendia Serda belendia@gmail.com"

ADD ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY ./flare/staticfiles /usr/share/nginx/html/static/staticfiles
EXPOSE 8999
CMD ["nginx", "-g", "daemon off;"]