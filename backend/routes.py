from apis.altas import ns_altas
from apis.atendimento_individual import ns_atendimentos_individuais
from apis.atendimento_odontologico import ns_atendimentos_odontologicos
from apis.atendimentos import ns_atendimentos_hospitalares
from apis.cids import ns_cids
from apis.cities import ns_cidades
from apis.collections import ns_collection
from apis.default import ns_defaults
from apis.encaminhamentos import ns_encaminhamentos
from apis.files import ns_files
from apis.progress_status import ns_progress_bar
from apis.states import ns_estados
from apis.visitas_domiciliar import ns_atendimentos_domiciliar
from flask import Blueprint
from flask_restx import Api
from views.collections import CreateCollection
from views.er_model_views import ErModelView
from views.file_manager import DownloadFile, UploadCSV
from views.home import home

# Inicializar o Blueprint para as rotas das views
views_bp = Blueprint("views", __name__)
views_bp.add_url_rule("/", "home", home)
views_bp.add_url_rule("/upload_csv", view_func=UploadCSV.as_view("upload_csv"))
views_bp.add_url_rule("/download", view_func=DownloadFile.as_view("download"))
views_bp.add_url_rule(
    "/create_collection",
    view_func=CreateCollection.as_view("create_collection"),
)
views_bp.add_url_rule("/er_model", view_func=ErModelView.as_view("er_model"))

# Inicializar o Blueprint para as rotas da API
api_bp = Blueprint("api", __name__)
api = Api(
    api_bp,
    title="SISAB-DASH API's",
    version="1.0",
    description="API's para o projeto SISAB-DASH: https://sisab-dash.elsvital.dev/",
)

api.add_namespace(ns_altas, path="/v1")
api.add_namespace(ns_atendimentos_domiciliar, path="/v1")
api.add_namespace(ns_atendimentos_hospitalares, path="/v1")
api.add_namespace(ns_atendimentos_individuais, path="/v1")
api.add_namespace(ns_atendimentos_odontologicos, path="/v1")
api.add_namespace(ns_cids, path="/v1")
api.add_namespace(ns_cidades, path="/v1")
api.add_namespace(ns_collection, path="/v1")
api.add_namespace(ns_estados, path="/v1")
api.add_namespace(ns_encaminhamentos, path="/v1")
api.add_namespace(ns_defaults, path="/v1")
api.add_namespace(ns_files, path="/v1")
api.add_namespace(ns_progress_bar, path="/v1")


def init_app(app):
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
