import dash
import dash_bootstrap_components as dbc
from callbacks.utils.utils import estados_brasileiros
from constants import time_division
from dash import dcc, html

def Footer():
    return html.Div(
        id="footer",
        children=[
            html.Div([
                html.Div([
                    html.Img(
                        src=dash.get_asset_url("ime.svg"),
                        height="40px",
                    ),
                    html.Div([
                        html.A(
                            href="https://www.ime.usp.br/",
                            className=f"fa fa-globe icon-footer",
                        )
                    ], className="footer-icons")
                ], className="footer-institution-content"),
                html.Div([
                    html.Img(
                        src=dash.get_asset_url("logo-ieps.svg"),
                        height="40px",
                    ),
                    html.Div([
                        html.A(
                            href="https://ieps.org.br/",
                            className=f"fa fa-globe icon-footer",
                        ),
                        html.A(
                            href="https://www.instagram.com/iepsoficial/",
                            className=f"fa-brands fa-instagram icon-footer",
                        ),
                        html.A(
                            href="https://x.com/IEPSoficial",
                            className=f"fa-brands fa-twitter icon-footer",
                        ),
                        html.A(
                            href="https://br.linkedin.com/company/iepsoficial",
                            className=f"fa-brands fa-linkedin icon-footer",
                        )
                    ], className="footer-icons")
                ], className="footer-institution-content")
            ], className="footer-institution-box"),
            html.Div(
                [
                    html.Img(
                        src=dash.get_asset_url("copyleft.svg"),
                        height="15px",
                    ),
                    html.P (
                        "copyleft",
                        style={"margin-bottom": "0px", "color": "#ffffffab", "font-size": "10px", "padding-left": "5px"}
                    )
                ], style={"padding-top": "15px", "display": "flex", "align-items": "center"}
            )
        ]

    )