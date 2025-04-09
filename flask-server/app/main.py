from . import create_app
import logging
from flask.logging import default_handler

app = create_app()

@app.route("/test", methods=["GET"])
def test():
    """Health check endpoint to verify server status."""
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
