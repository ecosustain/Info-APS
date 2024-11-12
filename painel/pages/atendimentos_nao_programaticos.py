import dash
import dash_bootstrap_components as dbc
from api.api_requests import anos
from dash import dcc, html

dash.register_page(
    __name__,
    path="/atendimentos-nao-programaticos",
    title="Não Programáticos",
    name="Não Programáticos",
)
from components.map import Map

square_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#632956",
        "margin-right": "5px",
    }
)

rhombus_legend = html.Span(
    style={
        "display": "inline-block",
        "width": "8px",
        "height": "8px",
        "background-color": "#34679A",
        "transform": "rotate(45deg)",
        "margin-right": "5px",
    }
)

slash_column = dbc.Col(
    [
        html.Span(
            style={
                "display": "inline-block",
                "width": "1px",
                "height": "100%",
                "background-color": "#212529bf",
            }
        )
    ],
    className="slash",
)


def indicator_component(title, ind_brasil, ind_estado, ind):
    legend = html.Div([])

    if ind_brasil != None:
        legend = html.Div(
            className="indicator-legend-box",
            children=[
                html.Div(
                    className="indicator-legend",
                    children=[
                        square_legend,
                        html.P(id=ind_brasil, className="legend-text"),
                    ],
                ),
                html.Div(
                    className="indicator-legend",
                    children=[
                        rhombus_legend,
                        html.P(id=ind_estado, className="legend-text"),
                    ],
                ),
            ],
        )

    return dbc.Col(
        [
            dbc.Row(
                html.H4(
                    title,
                    className="description-indicator-small",
                ),
            ),
            legend,
            dbc.Row(
                html.Div(
                    className="indicator-footer",
                    children=[
                        html.H2(
                            id=ind,
                            className="indicator-number-small",
                        ),
                    ],
                ),
            ),
        ],
        className="indicator-column",
    )


layout = html.Div(
    [
        html.Div(
            id="indicators",
            children=[
                Map(),
                html.Div(
                    [
                        html.H2(
                            "Atendimentos Não Programáticos",
                            id="atendimentos-title",
                        ),
                        html.Div(
                            id="indicator-content",
                            children=[
                                dbc.ButtonGroup(
                                    [
                                        dbc.Button(
                                            str(ano),
                                            id=f"btn-ano-{ano}",
                                            color="primary",
                                            outline=True,
                                            active=(
                                                ano == anos[0]
                                            ),  # Define o primeiro ano como ativo
                                            className="year-button rounded",
                                        )
                                        for ano in anos
                                    ],
                                    vertical=False,  # Para deixar os botões lado a lado
                                ),
                                html.Div(
                                    className="indicator-legend-box",
                                    children=[
                                        html.Div(
                                            className="indicator-legend",
                                            children=[
                                                square_legend,
                                                html.P(
                                                    "Brasil",
                                                    className="legend-text",
                                                ),
                                            ],
                                        ),
                                        html.Div(
                                            className="indicator-legend",
                                            children=[
                                                rhombus_legend,
                                                html.P(
                                                    "Estado",
                                                    className="legend-text",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        indicator_component(
                                            "ASMA e DPOC",
                                            "indicador-asma-dpoc-brasil",
                                            "indicador-asma-dpoc-estado",
                                            "big-asma-dpoc",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Dengue",
                                            "indicador-dengue-brasil",
                                            "indicador-dengue-estado",
                                            "big-dengue",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Tuberculose",
                                            "indicador-tuberculose-brasil",
                                            "indicador-tuberculose-estado",
                                            "big-tuberculose",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        indicator_component(
                                            "DST",
                                            "indicador-dst-brasil",
                                            "indicador-dst-estado",
                                            "big-dst",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Hanseníase",
                                            "indicador-hanseniase-brasil",
                                            "indicador-hanseniase-estado",
                                            "big-hanseniase",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Febres",
                                            "indicador-febres-brasil",
                                            "indicador-febres-estado",
                                            "big-febres",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        indicator_component(
                                            "Febre",
                                            "indicador-febre-brasil",
                                            "indicador-febre-estado",
                                            "big-febre",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Cefaléia",
                                            "indicador-cefaleia-brasil",
                                            "indicador-cefaleia-estado",
                                            "big-cefaleia",
                                        ),
                                        slash_column,
                                        indicator_component(
                                            "Tosse",
                                            "indicador-tosse-brasil",
                                            "indicador-tosse-estado",
                                            "big-tosse",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                            ],
                        ),
                    ],
                    style={"width": "100%"},
                ),
            ],
        ),
        html.H2("Visão ao decorrer do tempo", id="overview", className="mt-3"),
        html.Div(
            id="year-content",
            className="time-visualization-content",
            children=[
                dbc.Row(
                    [
                        # Asma + DPOC por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Asma e DPOC",
                                    id="asma-dpoc-title",
                                ),
                                dcc.Graph(
                                    id="chart_asma_dpoc_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Dengue por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Dengue",
                                    id="dengue-title",
                                ),
                                dcc.Graph(
                                    id="chart_dengue_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Tuberculose por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Tuberculose",
                                    id="tuberculose-title",
                                ),
                                dcc.Graph(
                                    id="chart_tuberculose_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # DST por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de DST",
                                    id="dst-title",
                                ),
                                dcc.Graph(
                                    id="chart_dst_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Hanseniase por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Hanseníase",
                                    id="hanseniase-title",
                                ),
                                dcc.Graph(
                                    id="chart_hanseniase_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Febres por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Febres",
                                    id="febres-title",
                                ),
                                dcc.Graph(
                                    id="chart_febres_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Febre por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Febre",
                                    id="febre-title",
                                ),
                                dcc.Graph(
                                    id="chart_febre_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Cefaleia por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Cefaleia",
                                    id="cefaleia-title",
                                ),
                                dcc.Graph(
                                    id="chart_cefaleia_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                        # Tosse por população
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Tosse",
                                    id="tosse-title",
                                ),
                                dcc.Graph(
                                    id="chart_tosse_by_year",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=4,
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="quarter-content",
            className="time-visualization-content",
            children=[
                dbc.Row(
                    [
                        # Asma + DPOC por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Asma e DPOC por Trimestre",
                                    id="asma-dpoc-title",
                                ),
                                dcc.Graph(
                                    id="chart_asma_dpoc_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # Dengue por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Dengue por Trimestre",
                                    id="dengue-title",
                                ),
                                dcc.Graph(
                                    id="chart_dengue_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Tuberculose por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Tuberculose por Trimestre",
                                    id="tuberculose-title",
                                ),
                                dcc.Graph(
                                    id="chart_tuberculose_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # DST por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de DST por Trimestre",
                                    id="dst-title",
                                ),
                                dcc.Graph(
                                    id="chart_dst_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Hanseniase por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Hanseníase por Trimestre",
                                    id="hanseniase-title",
                                ),
                                dcc.Graph(
                                    id="chart_hanseniase_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # Febres por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Febres por Trimestre",
                                    id="febres-title",
                                ),
                                dcc.Graph(
                                    id="chart_febres_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Febre por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Febre por Trimestre",
                                    id="febre-title",
                                ),
                                dcc.Graph(
                                    id="chart_febre_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                        # Cefaleia por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Cefaleia por Trimestre",
                                    id="cefaleia-title",
                                ),
                                dcc.Graph(
                                    id="chart_cefaleia_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        # Tosse por trimestre
                        dbc.Col(
                            [
                                html.H6(
                                    "Atendimentos de Tosse por Trimestre",
                                    id="tosse-title",
                                ),
                                dcc.Graph(
                                    id="chart_tosse_by_quarter",
                                    style={"height": "40vh"},
                                ),
                            ],
                            width=6,
                        ),
                    ],
                ),
            ],
        ),
    ]
)
