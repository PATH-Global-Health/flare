FROM nginx:latest
ADD ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./frontend/build /usr/share/nginx/html
COPY ./staticfiles /usr/share/nginx/html/static/staticfiles