# Dinkleberg's Auction House

## TODO

### React Frontend

1. Analytics & Reports
2. Manage Users
3. Site Settings
4. Other UI
    1. Stripe Payments
    2. Friend
    3. View Profile
    4. Live Auction

### Flask Server

1. MySQL
    1. Foreign Keys
    2. Payment Info Table
    3. Models Table
    4. Direct Transaction to Payment Info ID
    5. Listings Should Have Count
2. Logging
3. Analytics & Reports
4. Order & Delivery API
5. Payment API

## Setup

1. Ensure you have [Node.js](https://nodejs.org/en/download) installed on your machine.

### React Frontend

1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm install` command to install node modules and required packages within the `package.json` file.

### Flask Server

1. In a terminal, change to the `flask-server` directory.
2. Run the `python -m venv .venv` command to install a virtual environment.
3. Run the `.venv/Scripts/activate` command to activate the virtual environment.
4. Run the `pip install -r requirements.txt` command to install the necessary dependencies.

## Usage

### React Frontend

1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm run dev` command to launch the React app.

### React Testing

1. In a terminal, change to the `react-frontend` directory.
2. Run the `npm test` command to run tests.

### Flask Backend

1. In a terminal, change to the `flask-server` directory.
2. Run the `.venv/Scripts/activate` command to activate the virtual environment.
3. Run the `flask run --debug` command to run the Flask server.

### Flask Testing

1. In a terminal, change to the `flask-server` directory.
2. Run the `pytest tests/ -W ignore::DeprecationWarning` command to run tests.
    1. We are ignoring depreciation warnings since they're for site-packages unrelated to our code.
