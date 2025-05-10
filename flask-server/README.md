# Flask Server

## Setup

1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install -r requirements.txt` command to install the necessary dependencies.

## Usage

1. In a terminal, change to the `flask-server` directory.
2. Run the `.venv/Scripts/activate` command to activate the virtual environment.
3. Run the `python -m app.main` command to run the Flask server.

## Testing

1. In a terminal, change to the `flask-server` directory.
2. Run the `pytest tests/ -W ignore::DeprecationWarning` command to run tests.
    1. We are ignoring depreciation warnings since they're for site-packages unrelated to our code.
