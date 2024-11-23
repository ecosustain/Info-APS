from flask_restx import Resource, Namespace
from helpers.progress_bar import ProgressManager
from flask import make_response, jsonify, request

ns_progress_bar = Namespace("Progress Bar", description="Operações para controle da barra de progresso nas páginas")

@ns_progress_bar.route("/progress/<progress_id>", strict_slashes=False)
class ProgressBarStatus(Resource):
    def get(self, progress_id):
        """
        :return: states data as a response with HTTP status code 200 if successful, or an error message with HTTP status code 500
        """
        try:
            progress_manager = ProgressManager()
            progress = progress_manager.get_progress(progress_id)
            response = make_response(jsonify(progress), 200)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_progress_bar.route("/progress/progress_start", strict_slashes=False)
class ProgressBarStart(Resource):
    def get(self):
        """
        :return: states data as a response with HTTP status code 200 if successful, or an error message with HTTP status code 500
        """
        try:
            progress_manager = ProgressManager()

            response = make_response(jsonify({"progress_id": progress_manager.start_progress()}), 200)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)


@ns_progress_bar.route("/progress/progress_reset", strict_slashes=False)
class ProgressBarReset(Resource):
    def get(self, progress_id):
        """
        :return: states data as a response with HTTP status code 200 if successful, or an error message with HTTP status code 500
        """
        try:
            progress_manager = ProgressManager()
            progress = progress_manager.reset_progress(progress_id)
            response = make_response(jsonify({'progress': progress}), 200)
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
            return response

        except Exception as e:
            return make_response(jsonify({"error": str(e)}), 500)
