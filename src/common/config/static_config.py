from os import path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


class StaticConfig:

    @staticmethod
    def setup(app: FastAPI):
        app.mount("/static", StaticFiles(directory="public/static"), name="static")
