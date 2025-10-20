# Use Python 3.13 as the base image (adjust if necessary)
FROM python:3.13

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container (including main.py and run.py)
COPY . .

# This script reads the $PORT environment variable
CMD ["python", "main.py"]