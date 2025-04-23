from flask import jsonify, Response

import os, re

from ..utils.logger import setup_logger

logger = setup_logger(name="log_logger", log_file="logs/log.log")


class LogService:
    @staticmethod
    def list_logs():
        """
        Retrieve a list of available log files.

        Returns:
            Response: JSON response with a list of log filenames and HTTP 200 status code.
        """
        logs = [f for f in os.listdir("logs") if f.endswith(".log")]

        response_data = {"message": "Logs successfully retrieved", "logs": logs}
        logger.info(msg=f"Logs found: {[log for log in logs]}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")

    @staticmethod
    def get_log_file(filename: str, args: dict):
        """
        Retrieve the contents of a specific log file, optionally filtered by log level, date,
        line count, and maximum line length.

        Args:
            filename (str): The name of the log file to retrieve.
            args (dict): Dictionary of query parameters.

        Returns:
            Response: JSON response containing the filtered log content and HTTP status code.
        """
        level = args.get("level")
        date = args.get("date")
        max_line_length = args.get("line_length")
        limit = args.get("limit")

        if ".." in filename or not filename.endswith(".log"):
            response_data = {"error": "Invalid filename"}
            logger.error(msg=f"Invalid filename: {filename}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        filepath = f"logs/{filename}"
        if not os.path.isfile(filepath):
            response_data = {"error": "File not found"}
            logger.error(msg=f"Log: {filename} not found")
            return Response(response=jsonify(response_data).get_data(), status=404, mimetype="application/json")

        with open(filepath, "r") as f:
            log = f.readlines()

        try:
            if level:
                level_pattern = re.compile(rf"\b{re.escape(level)}\b", re.IGNORECASE)
                log = [line for line in log if level_pattern.search(line)]
        except re.error as e:
            response_data = {"error": "Invalid log level pattern"}
            logger.error(msg=f"Regex error for level filter: {e}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        try:
            if date:
                date_pattern = re.compile(rf"^{re.escape(date)}\b")
                log = [line for line in log if date_pattern.match(line)]
        except re.error as e:
            response_data = {"error": "Invalid date pattern"}
            logger.error(msg=f"Regex error for date filter: {e}")
            return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        if max_line_length:
            try:
                max_line_length = int(max_line_length)
                log = [line[:max_line_length] for line in log]
            except ValueError:
                response_data = {"error": "Invalid line_length value"}
                logger.error(msg="Invalid line_length parameter")
                return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        if limit:
            try:
                limit = int(limit)
                log = log[:limit]
            except ValueError:
                response_data = {"error": "Invalid limit value"}
                logger.error(msg="Invalid limit parameter")
                return Response(response=jsonify(response_data).get_data(), status=400, mimetype="application/json")

        response_data = {"message": "Log file successfully retrieved", "log": log}
        logger.info(msg=f"Returning {len(log)} lines from log: {filename}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
