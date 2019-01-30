FROM debian:9
COPY . /v2ray
WORKDIR /v2ray

RUN chmod +x /v2ray/multi-v2ray.sh;/v2ray/multi-v2ray.sh;
CMD [ "tail","-f" ]
