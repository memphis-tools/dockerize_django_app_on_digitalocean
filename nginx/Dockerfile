FROM nginxinc/nginx-unprivileged:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY --chown=nginx:root default.conf /etc/nginx/conf.d/default.conf
