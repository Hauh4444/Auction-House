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
        logger.info(msg=f"Logs found: {logs}")
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

        log_lines = []
        try:
            with open(filepath, "r") as f:
                for line in f:
                    # Apply filters in a single pass
                    if level and not re.search(rf"\b{re.escape(level)}\b", line, re.IGNORECASE):
                        continue
                    if date and not re.match(rf"^{re.escape(date)}\b", line):
                        continue
                    if max_line_length:
                        line = line[:int(max_line_length)]  # Truncate to max length if specified
                    log_lines.append(line)

                    if limit and len(log_lines) >= int(limit):  # Stop once we hit the limit
                        break

        except Exception as e:
            response_data = {"error": "Error reading log file"}
            logger.error(msg=f"Error reading log file: {e}")
            return Response(response=jsonify(response_data).get_data(), status=500, mimetype="application/json")

        response_data = {"message": "Log file successfully retrieved", "log": log_lines}
        logger.info(msg=f"Returning {len(log_lines)} lines from log: {filename}")
        return Response(response=jsonify(response_data).get_data(), status=200, mimetype="application/json")
