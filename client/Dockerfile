# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install the 'openai' package, which can talk to Ollama's API
RUN pip install openai

# Copy the Python script into the container at /app
COPY run_query.py .

# When the container launches, run the python script
CMD ["python", "run_query.py"]
