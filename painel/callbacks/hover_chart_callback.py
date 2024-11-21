"""Função para registrar os callbacks de hover nos gráficos"""

from dash import Input, Output, State, clientside_callback, set_props


def callback(app):
    """Função para registrar os callbacks de hover nos gráficos"""

    def hover_event_template(id_chart):
        """Função para criar o callback de hover nos gráficos"""
        
        clientside_callback(
            """
            function(hoverData, currentFigure) {
                var figureChart = JSON.parse(JSON.stringify(currentFigure));
                if (!hoverData || !hoverData.points || hoverData.points.length === 0) {
                    figureChart.data[0].selectedpoints = null;
                } else {
                    const hoverPoint = hoverData.points[0].pointIndex;
                    figureChart.data[0].selectedpoints = [hoverPoint];
                }

                return figureChart
            }
            """,
            Output(id_chart, "figure", allow_duplicate=True),
            Input(id_chart, "hoverData"),
            [State(id_chart, "figure")],
            allow_duplicate=True,
            prevent_initial_call=True,
        )

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
    hover_event_template("chart_cefaleia_by_year")
    hover_event_template("chart_tosse_by_year")
    hover_event_template("chart_asma_dpoc_by_quarter")
    hover_event_template("chart_dengue_by_quarter")
    hover_event_template("chart_tuberculose_by_quarter")
    hover_event_template("chart_dst_by_quarter")
    hover_event_template("chart_hanseniase_by_quarter")
    hover_event_template("chart_febres_by_quarter")
    hover_event_template("chart_cefaleia_by_quarter")
    hover_event_template("chart_tosse_by_quarter")
