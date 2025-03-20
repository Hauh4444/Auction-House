from . import create_app

app = create_app()


@app.route("/test", methods=["GET"])
def test():
    """Health check endpoint to verify server status."""
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
