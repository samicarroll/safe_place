# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install required dependencies for Chrome and chromedriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    ca-certificates \
    gnupg \
    dirmngr

# Install Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Install chromedriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip -P /tmp/ && \
    unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver_linux64.zip \
    
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY *.py /app/
COPY static /app/static/
COPY templates /app/templates/

# Install any needed packages specified in requirements.txt
# RUN pip3 freeze > requirements.txt  // unsure about this line
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=login.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run login.py when the container launches
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=80"]