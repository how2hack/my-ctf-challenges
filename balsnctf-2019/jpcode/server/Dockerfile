FROM ubuntu:16.04
MAINTAINER how2hack
RUN dpkg --add-architecture i386
RUN apt-get update --fix-missing
RUN apt-get install xinetd -y
RUN apt-get install python -y
RUN apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 -y
RUN useradd -m jpcode
RUN chmod 774 /tmp
RUN chmod -R 774 /var/tmp
RUN chmod -R 774 /dev
RUN chmod -R 774 /run
RUN chmod 1733 /tmp /var/tmp /dev/shm
COPY ./src /home/jpcode
RUN chown -R root:root /home/jpcode
COPY ./xinetd /etc/xinetd.d/xinetd
CMD ["/usr/sbin/xinetd","-dontfork"]
