# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Clone the GitHub repository with the FastAPI application code
RUN apt-get update && apt-get -y install git
RUN git clone https://github.com/BigDataIA-Spring2023-Team-12/FastAPI.git .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV OPENAI_API_KEY="key"
ENV PINECONE_API_KEY="key"
ENV PINECONE_ENV="key"

# Expose the port that the application will run on
EXPOSE 8000

# Start the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
