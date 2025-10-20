from fastapi.templating import Jinja2Templates
from fastapi.templating import Jinja2Templates


class TemplateConfig:

    templates = Jinja2Templates(directory="public/templates")
