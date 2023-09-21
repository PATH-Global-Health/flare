FROM nginx:latest
LABEL maintainer="Belendia Serda belendia@gmail.com"

ADD ./nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
COPY ./flare/config/staticfiles /usr/share/nginx/html/static
EXPOSE 8999
CMD ["nginx", "-g", "daemon off;"]