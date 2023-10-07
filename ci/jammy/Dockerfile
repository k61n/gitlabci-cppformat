# Version 0.0.2
FROM --platform=linux/amd64 ubuntu:jammy

WORKDIR /root

RUN apt update && apt upgrade -y

RUN apt install -y git wget \
	build-essential clang-tidy clang-format gawk \
	python3 libpython3-dev python3-pip python3-venv

#install latest cmake from ppa
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null && \
	echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ jammy main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null && \
	apt update && \
	apt install -y cmake

RUN python3 -m venv venv-cppformat

COPY files/ /
