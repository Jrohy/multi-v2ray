FROM centos:latest as builder

RUN curl -L -s https://install.direct/go.sh|bash

FROM alpine:latest

LABEL maintainer "Jrohy <euvkzx@Jrohy.com>"

ENV COMPLETION_FILE "/usr/share/bash-completion/completions/v2ray"

ENV SOURCE_COMPLETION_FILE "https://multi.netlify.com/v2ray"

ENV VERSION_LIST "https://api.github.com/repos/Jrohy/multi-v2ray/tags"

COPY --from=builder /usr/bin/v2ray/v2ray /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/v2ctl /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geoip.dat /usr/bin/v2ray/
COPY --from=builder /usr/bin/v2ray/geosite.dat /usr/bin/v2ray/
COPY run.sh /root

WORKDIR /root

RUN apk --no-cache add python3 bash bash-completion ca-certificates curl socat openssl iptables ip6tables && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    LATEST_VERSION=`curl -s $VERSION_LIST|grep name|grep -o "[0-9].*[0-9]"|head -n 1` && \
    pip install v2ray-util==$LATEST_VERSION && \
    curl $SOURCE_COMPLETION_FILE > $COMPLETION_FILE && \
    mkdir /var/log/v2ray/ && \
    chmod +x /usr/bin/v2ray/v2ctl && \
    chmod +x /usr/bin/v2ray/v2ray && \
    chmod +x /root/run.sh && \
    chmod +x $COMPLETION_FILE && \
    echo "source $COMPLETION_FILE" > /root/.bashrc && \
    ln -s $(which v2ray-util) /usr/local/bin/v2ray && \
    rm -r /root/.cache

ENTRYPOINT ["./run.sh"]