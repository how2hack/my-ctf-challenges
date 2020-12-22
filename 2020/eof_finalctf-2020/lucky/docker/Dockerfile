FROM ubuntu:18.04
MAINTAINER how2hack
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd -y
RUN apt-get install python3 -y
RUN useradd -m lucky
COPY ./share /home/lucky
COPY ./xinetd /etc/xinetd.d/lucky
COPY ./flag /flag
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/lucky
CMD ["/usr/sbin/xinetd","-dontfork"]
