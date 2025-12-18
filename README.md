# 🐍 Python MongoDB API Template

A **production-ready backend template** built with **FastAPI**, **MongoDB**, **Redis** and **MinIO**, designed for real-world applications.

This project follows well known architecture principles and provides a solid foundation for building scalable APIs with authentication, file storage, caching, observability and Docker support.

---

## ✨ Key Features

* ⚡ **FastAPI (async)** with Motor (MongoDB async driver)
* 🔐 **JWT Authentication** (access & refresh tokens)
* 🧠 **Redis integration**

  * Token blacklist
  * Caching support
* 📦 **MinIO object storage**

  * User attachments & files
  * S3-compatible storage
* 📧 Email service ready (SMTP)
* 🚦 Rate limiting middleware
* 📊 **Observability**

  * Prometheus metrics
  * Grafana dashboards
  * Jaeger tracing
* 🐳 Full **Docker & Docker Compose** setup
* 🩺 Healthcheck endpoint
* 🧪 Test-ready structure

---

## 🧰 Tech Stack

* **Python 3.11+**
* **FastAPI**
* **MongoDB**
* **Redis**
* **MinIO**
* **Docker / Docker Compose**
* **Prometheus / Grafana / Jaeger**

---

## ⚙️ Requirements

To run locally you need:

* Python **3.11+**
* MongoDB
* Redis
* MinIO Storage
* Docker (optional but recommended)
* Make (optional)

---

## 🚀 Getting Started (Local)

```bash
git clone https://github.com/ortiz-python-templates/python-mongodb-api.git
cd python-mongodb-api

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🔧 Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Main environment variables:

```env
APP_ENVIRONMENT=development
APP_PORT=5000

# MongoDB
MONGO_URI=mongodb://127.0.0.1:27017
MONGO_DATABASE=python_template_mongodb_api

# Redis
REDIS_URL=redis://localhost:6379

# JWT
JWT_SECRET_KEY=your_secret
JWT_REFRESH_SECRET_KEY=your_refresh_secret
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# MinIO
MINIO_ENDPOINT=localhost:9000
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin123
MINIO_MAIN_BUCKET=python-mongodb-bucket
```

---

## 🐳 Run with Docker (Recommended)

```bash
docker compose -f docker/docker-compose.yml up -d
```

This will start:

* FastAPI API
* MongoDB
* Redis
* MinIO
* Prometheus
* Grafana
* Jaeger

API Docs:
👉 [http://localhost:5000/docs](http://localhost:5000/docs)

MinIO Console:
👉 [http://localhost:9001](http://localhost:9001)

Grafana:
👉 [http://localhost:3000](http://localhost:3000)
(Default user: `admin` / password: `admin`)

---

## ▶️ Run Locally (Without Docker)

```bash
make run
```

or

```bash
uvicorn main:app --reload
```

---

## 🩺 Healthcheck (Complete and profissional)

```bash
GET /health
```

Response:

```json
{
	"status": "ok",
	"service": "python-template-mongodb-api",
	"version": "1.0.0",
	"environment": "development",
	"timestamp": "2025-12-18T12:48:14.387926Z",
	"uptime_seconds": 166,
	"hostname": "ortiz-latitude3379",
	"dependencies": {
		"mongodb": {
			"status": "up",
			"latency_ms": 8.79
		},
		"redis": {
			"status": "up",
			"latency_ms": 0.85
		}
	},
	"runtime": {
		"cpu_percent": 57.8,
		"memory_rss_mb": 105.58,
		"memory_vms_mb": 1006.89
	}
}
```

---

## 📂 Project Structure (Simplified)

```
src/
 ├── common/        # Configs, middlewares, storage, utils
 ├── core/          # Controllers, services, repositories
 ├── models/        # MongoDB models
 ├── schemas/       # Request / response schemas
 ├── services/      # Business logic
 └── repositories/ # MongoDB query & command repositories
```

---

## 📁 File Storage Strategy

* Files are stored in **MinIO**
* Database stores only the **object_key**
* Access URLs are generated dynamically (public or signed URLs)
* Ready for:

  * User avatars
  * Attachments
  * Documents
  * Images

---

## 🧪 Tests

```bash
make test
```

---

## 🛠️ Make Commands

```bash
make help           # Help
make run            # Run API
make test           # Run tests
make clean_cache    # Clear Python cache
make docker_up      # Start Docker Compose
make docker_down    # Stop Docker Compose
```

---

## 📦 Use Cases

This template is suitable for:

* SaaS backends
* Admin dashboards
* Authentication services
* File-heavy systems
* Internal APIs
* Microservices foundations

---

## 🪪 License

MIT License © 2025
Built and maintained by **Ortiz David**

