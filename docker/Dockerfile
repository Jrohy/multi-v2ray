FROM centos:latest as builder

RUN curl -L -s https://install.direct/go.sh|bash

FROM alpine:latest

LABEL maintainer "Jrohy <euvkzx@Jrohy.com>"

WORKDIR /v2ray

COPY --from=builder /usr/bin/v2ray/* /usr/bin/v2ray/
COPY run.sh /v2ray

RUN apk --no-cache add python3 bash ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    pip install -U v2ray-util && \
    mkdir /var/log/v2ray/ && \
    chmod +x /usr/bin/v2ray/v2ctl && \
    chmod +x /usr/bin/v2ray/v2ray && \
    chmod +x /v2ray/run.sh && \
    ln -s $(which v2ray-util) /usr/local/bin/v2ray && \
    rm -r /root/.cache

ENTRYPOINT ["./run.sh"]