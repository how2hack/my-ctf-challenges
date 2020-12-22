FROM ubuntu:18.04
MAINTAINER how2hack
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd -y
RUN apt-get install python3 -y
RUN useradd -m unlucky
COPY ./share /home/unlucky
COPY ./xinetd /etc/xinetd.d/unlucky
COPY ./flag /
RUN chmod 0400 /flag
RUN chmod 4755 /readflag
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/unlucky
CMD ["/usr/sbin/xinetd","-dontfork"]
