FROM python:3.6.5-slim-jessie
#FROM python:2.7-slim-jessie
 
ENV DEBIAN_FRONTEND noninteractive 
 
RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests \ 
  vim \
  libqt4-network \
  libgomp1 \
  zlib1g \
  libstdc++6
  
RUN pip install numpy mypy pronto pytest jupyter pyopenms==2.3.*
 
