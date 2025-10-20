from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


def add_cors_middleware(app: FastAPI):
    origins = [
        "http://localhost",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://localhost:3000", 
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins, 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
