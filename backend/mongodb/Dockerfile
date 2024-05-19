# Use a base image with MongoDB pre-installed
FROM mongo:latest

COPY backup.sh backup.sh
# Install curl and the AWS CLI
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir awscli && \
    chmod +x backup.sh  && \
    mkdir usr/files/

# Set the default command to run MongoDB

CMD ["mongod", "--storageEngine", "wiredTiger", "--auth"]