FROM openjdk:8-jdk-alpine
MAINTAINER Massimo Santini "santini@di.unimi.it"
ARG userid=1000
RUN apk add --update python && rm -rf /var/cache/apk/*
RUN adduser -D -g "" -u $userid tmuser
COPY ./sf /bin/sf
COPY ./tm /bin/tm
RUN chmod a+rx /bin/sf && chmod a+rx /bin/tm
USER tmuser
ENV PYTHONPATH=/bin/sf:/bin/tm
ENTRYPOINT [ "/bin/sf" ]
CMD [ "tmtest", "-n", "-c", "/conf.py", "-u", "/uploads", "-r", "/results.json" ]
