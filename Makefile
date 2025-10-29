# ----------------------------------------------------------
# Python MongoDB API - Makefile
# ----------------------------------------------------------

VENV = .venv


# ----------------------------------------------------------
# Run
# ----------------------------------------------------------

run:
	python main.py


# ----------------------------------------------------------
# Clean
# ----------------------------------------------------------

clean_cache:
	@echo "Cleaning Python caches..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "Caches removed."

clean_venv:
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "Virtual environment removed."

clean_all: clean_cache clean_venv


# ----------------------------------------------------------
# Tests and Lint
# ----------------------------------------------------------

test:
	python -m unittest discover -s tests -p "*_test.py"

lint:
	@$(VENV)/bin/flake8 . || true


# ----------------------------------------------------------
# Docker
# ----------------------------------------------------------

docker_build:
	docker build -f docker/Dockerfile -t ortizdavid/python-mongodb-api:latest .

docker_push:
	docker push ortizdavid/python-mongodb-api:latest

docker_run:
	docker run -d --name python-mongodb-api -p 60061:60061 ortizdavid/python-mongodb-api:latest

docker_stop:
	docker stop python-mongodb-api || true

docker_rm:
	docker rm python-mongodb-api || true

docker_up:
	docker compose --env-file .env -f docker/docker-compose.yml up

docker_down:
	docker compose --env-file .env -f docker/docker-compose.yml down -v

docker_logs:
	docker compose logs -f

docker_restart:
	docker compose restart

docker_run_app:
	docker run -d \
	--name mongodb-api \
	--network mongodb-net 
	-p 5000:5000 \
	ortizdavid/python-mongodb-api:latest


docker_run_minio:
	docker run -d \
	--name minio \
	-p 9000:9000 \
	-p 9001:9001 \
	-e MINIO_ROOT_USER=admin \
	-e MINIO_ROOT_PASSWORD=admin123 \
	-v $(pwd)/minio-data:/data \
	minio/minio server /data --console-address ":9001"



# ----------------------------------------------------------
# Help
# ----------------------------------------------------------

help:
	@echo ""
	@echo "Available commands:"
	@echo "-------------------"
	@echo "run                - Run the main Python app"
	@echo "test               - Run all unit tests"
	@echo "lint               - Run flake8 linting"
	@echo "clean_cache        - Remove Python cache files"
	@echo "clean_venv         - Remove virtual environment"
	@echo "clean_all          - Full clean (cache + venv)"
	@echo ""
	@echo "Docker commands:"
	@echo "----------------"
	@echo "docker_build       - Build the Docker image"
	@echo "docker_push        - Push the image to Docker Hub"
	@echo "docker_run         - Run container from image"
	@echo "docker_stop        - Stop running container"
	@echo "docker_rm          - Remove stopped container"
	@echo "docker_up          - Start Docker Compose"
	@echo "docker_down        - Stop and remove Docker Compose containers"
	@echo "docker_logs        - Show Docker logs"
	@echo "docker_restart     - Restart Docker Compose services"
	@echo "docker_run_app     - Run app container manually"
	@echo ""
	@echo "Example:"
	@echo "  make run"
	@echo ""
