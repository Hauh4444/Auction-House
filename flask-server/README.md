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

## Environment Variables

Create a `.env` file here with the following format:
```dotenv
PROJECT_ROOT=./
MAIL_DEFAULT_SENDER=your_mailersend_default_sender
ENCRYPTED_MAILERSEND_API_TOKEN=your_encrypted_mailersend_api_token
CIPHER_ENCRYPTION_KEY=your_cipher_encryption_key
SECRET_KEY=your_secret_key
FLASK_CONFIG=app.config.DevelopmentConfig
LIMITER_STORAGE_URI=memory://
FRONTEND_URL=http://localhost:5173 (or whatever frontend url)
BACKEND_MODEL_URL=http://127.0.0.1:5000/static/models (or whatever backend url with /static/models)
DB_HOST=your_mysql_host
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB=your_mysql_db
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
```

## Testing

1. In a terminal, change to the `flask-server` directory.
2. Run the `pytest tests/ -W ignore::DeprecationWarning` command to run tests.
    1. We are ignoring depreciation warnings since they're for site-packages unrelated to our code.
