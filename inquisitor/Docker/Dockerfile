FROM debian
WORKDIR /inquisitor
RUN apt update -y ; apt upgrade -y
RUN apt install \
        libpcap-dev \
        nmap \
        tcpdump \
        iproute2 \
        -y
COPY ./build/test ./test
