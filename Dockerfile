FROM ubuntu:latest
LABEL authors="nanakusa"

ENTRYPOINT ["top", "-b"]