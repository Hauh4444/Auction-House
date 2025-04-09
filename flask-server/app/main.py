from . import create_app
import logging
from flask.logging import default_handler

app = create_app()
app.logger.setLevel(logging.INFO)

# Create a file handler
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handler
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
file_handler.setFormatter(formatter)

# Add the handler to app.logger
app.logger.addHandler(file_handler)

@app.route("/test", methods=["GET"])
def test():
    """Health check endpoint to verify server status."""
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
