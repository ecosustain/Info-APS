import warnings

import callbacks.hover_chart_callback as hover_chart
import callbacks.loading_callback as loading
import callbacks.population_callback as population
import callbacks.static_style_callback as static_style
from callbacks.filters import filter_dropdown, filter_season, filter_year
from callbacks.initial_informations import big_number_ii, charts_ii
from callbacks.map_chart import map_callback
from statsmodels.tools.sm_exceptions import ConvergenceWarning

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Non-invertible starting seasonal moving average",
)
warnings.filterwarnings("ignore", category=ConvergenceWarning)


def register_callbacks(app):
    """Função para registrar os callbacks do painel principal"""

    map_callback.callback(app)

    filter_year.callback(app)
    filter_dropdown.callback(app)
    filter_season.callback(app)

    big_number_ii.callback(app)
    charts_ii.callback(app)

    population.callback(app)

    static_style.callback(app)
    hover_chart.callback(app)
    loading.callback(app)
