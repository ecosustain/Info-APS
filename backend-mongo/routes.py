from flask import Blueprint
from flask_restx import Api

from apis.atendimento_individual import ns_atendimentos_individuais
from apis.atendimento_odontologico import ns_atendimentos_odontologicos
from apis.atendimentos import ns_atendimentos_hospitalares
from apis.encaminhamentos import ns_encaminhamentos
from apis.altas import ns_altas
from apis.cities import ns_cidades
from apis.files import ns_default
from apis.states import ns_estados
from apis.collections import ns_collection
from apis.visitas_domiciliar import ns_atendimentos_domiciliar
from views.home import home
from views.file_manager import UploadCSV, DownloadFile
from views.collections import CreateCollection
from views.er_model_views import ErModelView

# Inicializar o Blueprint para as rotas das views
views_bp = Blueprint('views', __name__)
views_bp.add_url_rule('/', 'home', home)
views_bp.add_url_rule('/upload_csv', view_func=UploadCSV.as_view('upload_csv'))
views_bp.add_url_rule('/download', view_func=DownloadFile.as_view('download'))
views_bp.add_url_rule('/create_collection', view_func=CreateCollection.as_view('create_collection'))
views_bp.add_url_rule('/er_model', view_func=ErModelView.as_view('er_model'))

# Inicializar o Blueprint para as rotas da API
api_bp = Blueprint('api', __name__)
api = Api(api_bp, title="SISAB-DASH API's", version="1.0", description="API's para o projeto SISAB-DASH: https://sisab-dash.elsvital.dev/")

api.add_namespace(ns_altas, path='/v1')
api.add_namespace(ns_atendimentos_domiciliar, path='/v1')
api.add_namespace(ns_atendimentos_hospitalares, path='/v1')
api.add_namespace(ns_atendimentos_individuais, path='/v1')
api.add_namespace(ns_atendimentos_odontologicos, path='/v1')
api.add_namespace(ns_cidades, path='/v1')
api.add_namespace(ns_collection, path='/v1')
api.add_namespace(ns_estados, path='/v1')
api.add_namespace(ns_encaminhamentos, path='/v1')
api.add_namespace(ns_default, path='/v1')


def init_app(app):
    app.register_blueprint(views_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
