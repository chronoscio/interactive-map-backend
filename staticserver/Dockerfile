FROM interactivemap:latest as interactivemap

FROM nginx:1.12.2-alpine

ADD server.conf /etc/nginx/conf.d/default.conf

COPY --from=interactivemap /appstatic /appstatic

