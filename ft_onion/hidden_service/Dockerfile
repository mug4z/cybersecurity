FROM alpine
# RUN apt install curl nginx openssl less -y
WORKDIR /hidden_service

RUN apk add nginx tor openssh-server openrc torsocks
COPY ./hidden_service/dockerfile_entrypoint.sh ./dockerfile_entrypoint.sh
COPY ./hidden_service/nginx.conf /etc/nginx/nginx.conf
COPY ./hidden_service/torrc ./tor/torrc
COPY ./hidden_service/ssh/sshd_config /etc/ssh/sshd_config
COPY ./hidden_service/ssh/tor.pub ./tor.pub
RUN  mkdir /root/.ssh ; cat ./tor.pub > /root/.ssh/authorized_keys
RUN chmod 744 dockerfile_entrypoint.sh 
ENTRYPOINT [ "./dockerfile_entrypoint.sh" ]

