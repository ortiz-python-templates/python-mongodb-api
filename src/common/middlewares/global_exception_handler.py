from src.common.config.log_config import Logger
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, PlainTextResponse
from src.common.utils.custom_exceptions import CustomException


class GlobalExceptionHandler:

    logger = Logger.get_logger(__name__)

    @staticmethod
    def setup(app: FastAPI):

        @app.exception_handler(CustomException)
        async def custom_exception(request: Request, exc: CustomException):
            exception_name = exc.__class__.__name__
            title = exc.title
            detail = exc.detail
            # Log diferenciado se desejar por tipo
            GlobalExceptionHandler.logger.warning(
                f"[{exception_name}] {detail} - Path: {request.url.path}"
            )
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "title": title,
                    "detail": detail,
                    "status": exc.status_code,
                    "path": str(request.url.path)
                }
            )


        @app.exception_handler(Exception)
        async def general_exception(request: Request, exc: Exception):
            GlobalExceptionHandler.logger.error(
                f"Unexpected Error: {str(exc)} - Path: {request.url.path}"
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "title": "Internal Server Error",
                    "detail": "An error occurred while processing request",
                    "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                    "path": str(request.url.path)
                }
            )