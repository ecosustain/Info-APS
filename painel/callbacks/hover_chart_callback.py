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
    hover_event_template("chart_hipertensao_by_year")
    hover_event_template("chart_diabetes_by_year")
    hover_event_template("chart_saude_sexual_by_year")
    hover_event_template("chart_saude_mental_by_year")
    hover_event_template("chart_puericultura_by_year")
    hover_event_template("chart_gravidez_by_year")
    hover_event_template("chart_hipertensao_by_quarter")
    hover_event_template("chart_diabetes_by_quarter")
    hover_event_template("chart_saude_sexual_by_quarter")
    hover_event_template("chart_saude_mental_by_quarter")
    hover_event_template("chart_puericultura_by_quarter")
    hover_event_template("chart_gravidez_by_quarter")
    hover_event_template("chart_asma_dpoc_by_year")
    hover_event_template("chart_dengue_by_year")
    hover_event_template("chart_tuberculose_by_year")
    hover_event_template("chart_dst_by_year")
    hover_event_template("chart_hanseniase_by_year")
    hover_event_template("chart_febres_by_year")
    hover_event_template("chart_febre_by_year")
    hover_event_template("chart_cefaleia_by_year")
    hover_event_template("chart_tosse_by_year")
    hover_event_template("chart_asma_dpoc_by_quarter")
    hover_event_template("chart_dengue_by_quarter")
    hover_event_template("chart_tuberculose_by_quarter")
    hover_event_template("chart_dst_by_quarter")
    hover_event_template("chart_hanseniase_by_quarter")
    hover_event_template("chart_febres_by_quarter")
    hover_event_template("chart_febre_by_quarter")
    hover_event_template("chart_cefaleia_by_quarter")
    hover_event_template("chart_tosse_by_quarter")
