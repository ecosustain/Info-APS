from dash import Input, Output, State


def callback(app):
    def hover_event_template(id_chart):
        @app.callback(
            Output(id_chart, "figure", allow_duplicate=True),
            Output("loading-graphics", "display", allow_duplicate=True),
            Input(id_chart, "hoverData"),
            [State(id_chart, "figure")],
            allow_duplicate=True,
            prevent_initial_call=True,
        )
        def callback(data, current_figure):
            traces = current_figure["data"]

            if data:
                hover_point = data["points"][0]["pointIndex"]

                for idx, trace in enumerate(traces):
                    trace.update({"selectedpoints": [hover_point]})
                    current_figure["data"][idx].update(trace)
            else:
                for idx, trace in enumerate(traces):
                    trace.update({"selectedpoints": None})
                    current_figure["data"][idx].update(trace)

            return current_figure, "hide"

    hover_event_template("mapa")
    hover_event_template("chart_by_year")
    hover_event_template("chart_encaminhamentos")
    hover_event_template("chart_odonto_by_year")
    hover_event_template("chart_visitas_by_year")
    hover_event_template("chart_by_year_profissionais")
    hover_event_template("chart_by_quarter")
    hover_event_template("chart_odonto_by_quarter")
    hover_event_template("chart_visitas_by_quarter")
