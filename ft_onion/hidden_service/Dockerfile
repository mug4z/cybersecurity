FROM alpine
# RUN apt install curl nginx openssl less -y
WORKDIR /hidden_service
RUN apk add nginx tor openssh-server
COPY ./hidden_service/dockerfile_entrypoint.sh ./dockerfile_entrypoint.sh
RUN chmod 744 dockerfile_entrypoint.sh
# COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
ENTRYPOINT [ "./dockerfile_entrypoint.sh" ]

