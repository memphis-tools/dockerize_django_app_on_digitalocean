FROM nginx:1.14.2-alpine

RUN apk update && apk add bash && rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
