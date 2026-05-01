FROM alpine:3.23
RUN apk update;\ 
  apk add --no-cache \
    # libcurl \
    curl \
    curl-dev\
    ca-certificates \
    libc-dev \
    gdb mandoc \
    man-pages \
    gcc ; \
  apk add docs
WORKDIR /spider
