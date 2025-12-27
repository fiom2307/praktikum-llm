from flask import Blueprint, jsonify
from services.form_settings_service import get_form_settings

form_settings_routes = Blueprint("form_settings_routes", __name__)

@form_settings_routes.route("/form_settings", methods=["GET"])
def read_form_settings():
    settings = get_form_settings()

    if not settings:
        return jsonify({
            "pretest_enabled": False,
            "posttest_enabled": False
        })

    return jsonify({
        "pretest_enabled": settings.pretest_enabled,
        "posttest_enabled": settings.posttest_enabled
    })
