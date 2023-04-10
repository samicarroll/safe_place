# Use the official Selenium Python image as a base image
FROM selenium/standalone-chrome:4.0.0

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
COPY *.py /app/
COPY static /app/static/
COPY templates /app/templates/

# Install any needed packages specified in requirements.txt
RUN sudo apt-get update && sudo apt-get install -y python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV FLASK_APP=login.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run login.py when the container launches
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]