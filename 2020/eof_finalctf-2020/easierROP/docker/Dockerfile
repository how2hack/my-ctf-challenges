FROM ubuntu:18.04
MAINTAINER how2hack
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install xinetd -y
RUN apt-get install libseccomp-dev -y
RUN useradd -m easierROP
COPY ./share /home/easierROP
COPY ./xinetd /etc/xinetd.d/easierROP
COPY ./flag /home/easierROP/flag
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
RUN chown -R root:root /home/easierROP
CMD ["/usr/sbin/xinetd","-dontfork"]
