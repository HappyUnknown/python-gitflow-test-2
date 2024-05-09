# Download python 3.9 from dockerhub
FROM python:3.9
# Specifying a working directory
WORKDIR /backend
# download & install dependencies
COPY requirements.txt /backend
RUN pip3 install --upgrade pip -r requirements.txt
# copy the directory with Dockerfile, 
# into working directory
COPY . /backend