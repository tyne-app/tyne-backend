from src.configuration.Settings import Settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_app():
    docs_url = "/v1/swagger" if Settings.ENVIRONMENT == 'Development' else None
    tittle = "API Tyne"
    version = "1.0.0"
    api_description = "Encargado de toda la lógica de negocio de la aplicación, configuración y conexiones a APIs " \
                      "externas "

    app = FastAPI(
        docs_url=docs_url,
        title=tittle,
        description=api_description,
        version=version
    )

    return app


def add_middlewares(app: FastAPI):
    origins = ["http://localhost:4200",
               "https://tyne-frontend-prod.herokuapp.com",
               "https://tyne-frontend-dev.herokuapp.com",
               "https://tyne.cl",
               "https://www.tyne.cl",
               "http://tyne.cl",
               "http://www.tyne.cl"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return app
