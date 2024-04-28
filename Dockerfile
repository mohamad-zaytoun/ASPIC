# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY src/ /app/

# Install the application dependencies
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000
# Define environment variable to enable debug mode
ENV FLASK_ENV=development

# Define the entry point for the container
CMD ["python", "run.py"]