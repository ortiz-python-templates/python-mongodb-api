# 🐍 Python MongoDB API

Production-ready Python + FastAPI + MongoDB application template.  
Built from real-world use cases with Redis caching and JWT authentication.

---

## 🚀 Features
- Async FastAPI app using **Motor** (async MongoDB driver)
- JWT authentication (access + refresh tokens)
- Redis integration (token blacklist, caching)
- Mail configuration ready
- Rate limiting middleware
- Docker support
- Healthcheck endpoint

---

## 🧰 Requirements

To run the project locally you need:

- **Python 3.11+**
- **MongoDB** (running locally or via Docker)
- **Redis** (for token blacklist and cache)
- *(optional)* **Make**

---

## ⚙️ Installation

```bash
git clone https://github.com/ortizdavid/python-mongodb-api.git
cd python-mongodb-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
````

---

## 🧩 Environment Variables

Copy `.env.example` to `.env` and adjust if needed:

```bash
cp .env.example .env
```

### Example `.env`

```env
ENVIRONMENT=development
PORT=6000

# Mongo
MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DATABASE=python-template-mongodb-api

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=test-token
JWT_REFRESH_SECRET_KEY=your_refresh_secret_key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Mail
MAIL_USERNAME=example@gmail.com
MAIL_PASSWORD=YOUR_MAIL_PASSWORD
MAIL_FROM=example@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# Rate Limit
RATE_LIMIT_MAX_REQUESTS=1000
RATE_LIMIT_WINDOW_SECONDS=3600

# Files
UPLOADS_PATH=uploads
UPLOADS_MAX_DOCS_SIZE=4
```

---

## 🐳 Run with Docker

```bash
docker compose -f docker/docker-compose.yml up -d
```

This will start:

* FastAPI backend
* MongoDB
* Redis

Then visit:
👉 [http://localhost:5000/docs](http://localhost:5000/docs)

---

## 🩺 Healthcheck

To check if the app is running correctly:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{ "status": "ok", "service": "python-mongodb-api" }
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🧰 Make Commands (optional)

If you have **make** installed:

```bash
make run          # Start the API
make docker_up    # Run with Docker
make test         # Run tests
make clean_cache  # Clear Python cache
make test
```

---

## 📂 Project Structure

```
src/
 ├── common/        # Helpers, messages, constants
 └── core/          # App init, routers, middlewares, etc.
database/           # Mongo connection setup
docker/             # Docker config files
scripts/            # Maintenance scripts
tests/              # Unit tests
main.py             # App entrypoint
```

---

## 🧑‍💻 Development

Run locally with:

```bash
uvicorn main:app --reload
```

Docs available at:
👉 [http://localhost:5000/docs](http://localhost:5000/docs)

---

## 🪪 License

MIT License © 2025

```
