from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorDatabase
from src.common.middlewares.rate_limiter_middleware import RateLimiterMiddleware
from src.common.middlewares.global_exception_handler import GlobalExceptionHandler
from src.common.middlewares.authentication_middleware import AuthenticationMiddleware
from src.common.middlewares.cors_midleware import add_cors_middleware


class MiddlewareSetup:

    def setup(app: FastAPI, db: AsyncIOMotorDatabase):
        # Primeiro a autenticação
        app.add_middleware(AuthenticationMiddleware, db)

        app.add_middleware(RateLimiterMiddleware)

        # CORS, para que seja executado antes da autenticação
        add_cors_middleware(app)

        GlobalExceptionHandler.setup(app)
