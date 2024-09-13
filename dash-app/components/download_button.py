from dash import html, dcc

def create_download_button():
    return html.Div([
        html.Div([
            html.Button("Download CSV", id="btn_csv"),
            dcc.Download(id="download-dataframe-csv"),
        ], className='button download-button'),
    ])

