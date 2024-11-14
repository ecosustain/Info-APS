import dash
from dash import dcc, html


def SideBar():
    return html.Div(
        id="side-bar",
        children=[
            html.Div(
                [
                    html.Img(
                        src=dash.get_asset_url("sisab.svg"),
                        height="20px",
                    ),
                    html.P(
                        "SISAB + IEPS",
                        className="fs-6 px-2 py-0 text-white",
                        id="title",
                        style={"margin-bottom": "0px"}
                    ),
                ],
                className="px-4 d-flex",
                style={
                    "margin-bottom": "60px",
                    "display": "flex !important",
                    "align-items": "center",
                },
            ),
            html.Div (
                [
                    html.Div(
                        [
                            html.Div(
                                dcc.Link(
                                    f"{page['name']}",
                                    href=page["relative_path"],
                                    id=page["path"],
                                    className=f"btn",
                                )
                            )
                            for page in dash.page_registry.values()
                        ]
                    ),
                    html.Div(
                        dcc.Link(
                            "Serviços de dados",
                            href="https://dash-saude-mongo.elsvital.dev/",
                            className="btn",
                            target="_blank",
                        ),
                        style={"margin-top": "60px"}
                    )
                ],
                style={"display": "flex", "flex-direction": "column", "justify-content": "space-between"}
            )
        ],
    )
