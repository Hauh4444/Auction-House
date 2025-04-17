from flask import jsonify, Response

import os, re

from ..utils.logger import setup_logger

auth_logger = setup_logger(name="auth_logger", log_file="logs/auth.log")


class LogService:
    @staticmethod
    def list_logs():
        logs = [f for f in os.listdir("logs") if f.endswith(".log")]

        response_data = {"message": "Logs successfully retrieved", "logs": logs}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")


    @staticmethod
    def get_log_file(filename, args):
        level = args.get("level")
        date = args.get("date")

        if ".." in filename or not filename.endswith(".log"):
            response_data = {"error": "Invalid filename"}
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        filepath = f"logs/{filename}"
        if not os.path.isfile(filepath):
            response_data = {"error": "File not found"}
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        with open(filepath, "r") as f:
            log = f.readlines()

        if level:
            level_pattern = re.compile(rf"\b{re.escape(level)}\b", re.IGNORECASE)
            log = [line for line in log if level_pattern.search(line)]

        if date:
            date_pattern = re.compile(rf"^{re.escape(date)}\b")
            log = [line for line in log if date_pattern.match(line)]

        response_data = {"message": "Log file successfully retrieved", "log": log}
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")