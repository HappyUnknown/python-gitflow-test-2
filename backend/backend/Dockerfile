# Download python 3.9 from dockerhub
FROM python:3.9-slim
# Specifying a working directory
WORKDIR /backend
# download & install dependencies
ADD . /backend
RUN pip3 install --upgrade pip --no-cache-dir -r requirements.txt
CMD ["flask", "run"]





