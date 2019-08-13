FROM python:3.6.5-slim-jessie
#FROM python:2.7-slim-jessie
 
ENV DEBIAN_FRONTEND noninteractive 
 
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \ 
  vim \
  libqt4-network \
  libgomp1 \
  zlib1g \
  libstdc++6 \
  sudo \
  git
  
RUN pip install numpy mypy pronto pytest jupyter pyopenms==2.3.*
#RUN pip install -e .  # devcontainer.json: "postCreateCommand": "pip install -e .",

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME 
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME
    
#USER 1000  # "runArgs": ["-u", "1000"]
#extrawurst fuer vscode
#RUN mkdir -p /root