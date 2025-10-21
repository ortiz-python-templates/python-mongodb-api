# Lightweight and stable base image
FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy only the requirements first (better cache efficiency)
COPY requirements.txt .

# Install system dependencies (if needed) and Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

# Set default port variable (in case .env is not loaded)
ENV APP_PORT=5000

# Expose the application port
EXPOSE ${APP_PORT}

# Run the FastAPI server with Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${APP_PORT}"]
