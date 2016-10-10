FROM ubuntu:latest
MAINTAINER Matt Molo "Matt Molo"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# Copy current dir to /app and install things
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# Runs on port 4000
EXPOSE 4000
ENV FLASK_APP busser.py
CMD ["python", "busser.py"]
