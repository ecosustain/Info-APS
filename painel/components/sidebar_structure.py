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
                    ),
                ],
                className="pt-3 px-4 d-flex",
                style={
                    "margin-bottom": "60px",
                },
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Link(
                            f"{page['name']}",
                            href=page["relative_path"],
                            className="btn",
                        )
                    )
                    for page in dash.page_registry.values()
                ]
            ),
        ],
        className="p-0",
    )
